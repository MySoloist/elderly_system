import os
from dotenv import load_dotenv

# 获取backend目录
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 加载backend目录下的.env文件
env_path = os.path.join(backend_dir, ".env")
print(f"Loading .env from: {env_path}")

# 加载环境变量
load_dotenv(dotenv_path=env_path)

class Settings:
    APP_NAME = os.getenv("APP_NAME", "Elderly Food Delivery System")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/elderly_food_delivery")
    SECRET_KEY = os.getenv("SECRET_KEY", "test-secret-key")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "120"))
    BACKEND_CORS_ORIGINS = ["http://localhost:5173", "http://localhost:5174", "http://127.0.0.1:5173", "http://127.0.0.1:5174"]
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # DeepSeek AI配置
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
    DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com")
    DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    
    # 高德地图配置
    AMAP_API_KEY = os.getenv("AMAP_API_KEY", "")
    
    # 微信小程序配置
    WECHAT_APPID = os.getenv("WECHAT_APPID", "wx7d3e013a04e71938")
    WECHAT_SECRET = os.getenv("WECHAT_SECRET", "2e692ca19e81b4dd92735259bf5af7ba")
    WECHAT_LOGIN_URL = os.getenv("WECHAT_LOGIN_URL", "https://api.weixin.qq.com/sns/jscode2session")
    
    # 阿里云智能语音配置（用于前端语音识别和语音合成）
    ALIYUN_AKID = os.getenv("ALIYUN_AKID", "")
    ALIYUN_AKKEY = os.getenv("ALIYUN_AKKEY", "")
    ALIYUN_APPKEY = os.getenv("ALIYUN_APPKEY", "")

settings = Settings()