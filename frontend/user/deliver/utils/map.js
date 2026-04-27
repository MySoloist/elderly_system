// 地图工具函数

// 计算两个坐标点之间的距离（使用Haversine公式）
export function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // 地球半径（公里）
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  const distance = R * c;
  return distance;
}

function toRad(value) {
  return value * Math.PI / 180;
}

// 格式化距离显示
export function formatDistance(distance) {
  if (distance < 1) {
    return `距离${Math.round(distance * 1000)}m`;
  }
  return `距离${distance.toFixed(1)}km`;
}

// 估算送达时间（基于距离和平均速度）
export function estimateDeliveryTime(distance) {
  const avgSpeed = 25; // 平均速度（公里/小时）
  const timeHours = distance / avgSpeed;
  const timeMinutes = Math.round(timeHours * 60);
  
  const now = new Date();
  const deliveryTime = new Date(now.getTime() + timeMinutes * 60000);
  
  return deliveryTime.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  });
}

// 地址解析（模拟实现，实际项目中应该调用地图API）
export async function geocode(address) {
  // 在实际项目中，这里应该调用高德地图的地理编码API
  // 现在返回模拟数据，使用更小的随机范围
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        latitude: 39.9042 + (Math.random() * 0.02 - 0.01),
        longitude: 116.4074 + (Math.random() * 0.02 - 0.01)
      });
    }, 500);
  });
}

// 路径规划（模拟实现）
export async function calculateRoute(startLat, startLon, endLat, endLon) {
  // 在实际项目中，这里应该调用高德地图的路径规划API
  return new Promise((resolve) => {
    setTimeout(() => {
      const distance = calculateDistance(startLat, startLon, endLat, endLon);
      resolve({
        distance: distance,
        duration: distance / 25 * 60, // 时间（分钟）
        path: [] // 路径点数组
      });
    }, 1000);
  });
}

// 初始化高德地图插件
export function initAMap() {
  // 在实际项目中，这里应该初始化高德地图小程序插件
  console.log('高德地图插件初始化');
}