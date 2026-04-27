import requests
from sqlalchemy.orm import Session
from app.models import User, ElderlyProfile, MemberProfile, DelivererProfile, AdminProfile, UserType
from app.core.security import verify_password, get_password_hash
from app.core.config import settings

class AuthService:
    def authenticate_user(self, db: Session, username: str, password: str):
        print(f"认证用户: {username}")
        from sqlalchemy.orm import joinedload
        user = db.query(User).options(joinedload(User.deliverer_profile)).filter(User.username == username).first()
        if not user:
            print(f"用户不存在: {username}")
            return False
        print(f"找到用户: {user.username}, 用户类型: {user.user_type}")
        print(f"配送员档案: {user.deliverer_profile}")
        if not verify_password(password, user.password_hash):
            print(f"密码验证失败: {username}")
            return False
        print(f"密码验证成功: {username}")
        return user
    
    def change_password(self, db: Session, user: User, old_password: str, new_password: str):
        if not verify_password(old_password, user.password_hash):
            return False
        user.password_hash = get_password_hash(new_password)
        db.commit()
        db.refresh(user)
        return True
    
    def register_user(self, db: Session, username: str, password: str, user_type: str, profile_data: dict):
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            return None
        
        # 创建用户
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            password_hash=hashed_password,
            user_type=UserType(user_type.lower())  # 使用枚举类型
        )
        db.add(user)
        db.flush()  # 获取用户ID但不提交事务
        
        # 创建对应类型的用户档案
        if user_type.lower() == "elderly":
            profile = ElderlyProfile(
                user_id=user.id,
                name=profile_data.get('name'),
                phone=profile_data.get('phone'),
                age=profile_data.get('age'),
                gender=profile_data.get('gender')
            )
        elif user_type.lower() == "member":
            profile = MemberProfile(
                user_id=user.id,
                name=profile_data.get('name'),
                phone=profile_data.get('phone')
            )
        elif user_type.lower() == "deliverer":
            profile = DelivererProfile(
                user_id=user.id,
                name=profile_data.get('name'),
                phone=profile_data.get('phone')
            )
        elif user_type.lower() == "admin":
            profile = AdminProfile(
                user_id=user.id,
                name=profile_data.get('name'),
                phone=profile_data.get('phone')
            )
        else:
            db.rollback()
            return None
        
        db.add(profile)
        db.commit()
        db.refresh(user)
        return user
    
    def wechat_login(self, db: Session, code: str, user_type: str):
        print(f"开始微信登录流程，用户类型: {user_type}")
        print(f"微信AppID: {settings.WECHAT_APPID}")
        print(f"微信登录URL: {settings.WECHAT_LOGIN_URL}")
        print(f"获取到的code: {code}")
        
        # 调用微信API获取openid和session_key
        params = {
            'appid': settings.WECHAT_APPID,
            'secret': settings.WECHAT_SECRET,
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        
        print(f"请求参数: {params}")
        
        try:
            response = requests.get(settings.WECHAT_LOGIN_URL, params=params, timeout=10)
            print(f"微信API响应状态码: {response.status_code}")
            print(f"微信API响应内容: {response.text}")
            
            result = response.json()
            print(f"解析后的响应: {result}")
            
            if 'errcode' in result:
                print(f"微信API返回错误: errcode={result['errcode']}, errmsg={result.get('errmsg', '未知错误')}")
                raise Exception(f"微信登录失败: {result.get('errmsg', '未知错误')}, errcode={result['errcode']}")
            
            openid = result.get('openid')
            unionid = result.get('unionid')
            
            print(f"获取到的openid: {openid}")
            print(f"获取到的unionid: {unionid}")
            
            if not openid:
                raise Exception("微信登录失败: 无法获取openid")
                
        except Exception as e:
            print(f"微信API调用异常: {str(e)}")
            raise
        
        # 先尝试根据openid查找用户
        user = db.query(User).filter(User.openid == openid).first()
        
        if not user:
            # 如果没有找到，尝试查找同类型的未绑定微信的用户
            # 这里可以根据实际需求调整查找条件
            user = db.query(User).filter(
                User.user_type == UserType(user_type.lower()),
                User.openid.is_(None)
            ).first()
            
            if user:
                # 为已有用户绑定微信openid
                user.openid = openid
                user.unionid = unionid
                db.commit()
                db.refresh(user)
            else:
                # 创建新用户
                username = f"wx_{openid[:8]}"
                password_hash = get_password_hash(f"wx_{openid}")
                
                user = User(
                    username=username,
                    password_hash=password_hash,
                    openid=openid,
                    unionid=unionid,
                    user_type=UserType(user_type.lower())
                )
                db.add(user)
                db.flush()
                
                # 创建对应类型的用户档案
                if user_type.lower() == "elderly":
                    profile = ElderlyProfile(
                        user_id=user.id,
                        name=f"微信用户{openid[:4]}",
                        phone=None
                    )
                elif user_type.lower() == "member":
                    profile = MemberProfile(
                        user_id=user.id,
                        name=f"微信用户{openid[:4]}",
                        phone=None
                    )
                elif user_type.lower() == "deliverer":
                    profile = DelivererProfile(
                        user_id=user.id,
                        name=f"微信用户{openid[:4]}",
                        phone=None
                    )
                else:
                    db.rollback()
                    raise Exception(f"不支持的用户类型: {user_type}")
                
                db.add(profile)
                db.commit()
                db.refresh(user)
        
        return user

auth_service = AuthService()