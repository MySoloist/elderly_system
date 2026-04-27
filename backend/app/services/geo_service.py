from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Tuple, Optional
import requests

from app.models.user import ElderlyProfile
from app.core.config import settings

class GeoService:
    def __init__(self):
        self.geo_api_key = settings.AMAP_API_KEY
        self.base_url = "https://restapi.amap.com/v3"
    
    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        """
        将地址转换为经纬度坐标
        """
        if not self.geo_api_key:
            return None
        
        url = f"{self.base_url}/geocode/geo"
        params = {
            "address": address,
            "key": self.geo_api_key,
            "output": "json"
        }
        
        try:
            response = requests.get(url, params=params)
            result = response.json()
            
            if result.get("status") == "1" and result.get("geocodes"):
                location = result["geocodes"][0]["location"]
                longitude, latitude = map(float, location.split(","))
                return latitude, longitude
            return None
        except Exception as e:
            print(f"地址解析失败: {e}")
            return None
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        使用Haversine公式计算两点之间的距离（米）
        """
        from math import radians, cos, sin, asin, sqrt
        
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
        
        # haversine公式
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371000  # 地球平均半径，单位为米
        return c * r
    
    def get_nearby_elderly(self, db: Session, latitude: float, longitude: float, radius: float = 5000) -> list:
        """
        获取指定半径范围内的老人
        """
        from sqlalchemy.dialects.postgresql import func
        
        # 使用PostgreSQL的地理空间函数计算距离
        nearby_elderly = db.query(
            ElderlyProfile,
            func.ST_Distance(
                ElderlyProfile.location,
                func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
            ).label('distance')
        ).filter(
            ElderlyProfile.location.isnot(None),
            func.ST_DWithin(
                ElderlyProfile.location,
                func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326),
                radius
            )
        ).order_by('distance').all()
        
        return nearby_elderly
    
    def update_elderly_location(self, db: Session, elderly_id: int, latitude: float, longitude: float):
        """
        更新老人的位置信息
        """
        elderly = db.query(ElderlyProfile).filter(ElderlyProfile.user_id == elderly_id).first()
        if elderly:
            from sqlalchemy.dialects.postgresql import func
            elderly.location = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
            db.commit()
            return True
        return False

geo_service = GeoService()
