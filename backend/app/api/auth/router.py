from datetime import timedelta
from typing import Dict, Any, Union

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.config import settings
from app.core.security import create_access_token
from app.core.deps import get_current_active_user
from app.models import User
from app.schemas import Token, UserWithProfile, ChangePassword, ElderlyProfileResponse, MemberProfileResponse, DelivererProfileResponse, AdminProfileResponse, RegisterRequest, ElderlyProfileUpdate, MemberProfileUpdate, DelivererProfileUpdate, WechatLoginRequest
from app.services.auth_service import auth_service
from app.services.user_service import user_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 登录成功后设置配送员状态为在线
    print(f"用户类型: {user.user_type}, 类型: {type(user.user_type)}")
    print(f"用户类型字符串: {str(user.user_type)}")
    print(f"用户类型值: {user.user_type.value}")
    print(f"是否有配送员档案: {user.deliverer_profile is not None}")
    if user.user_type.value == "deliverer" and user.deliverer_profile:
        print(f"设置配送员 {user.username} 状态为 available")
        user.deliverer_profile.status = "available"
        db.commit()
        print("状态更新成功")
    else:
        print("跳过状态更新")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "user_type": user.user_type},
        expires_delta=access_token_expires
    )
    
    profile = None
    if user.user_type == "elderly" and user.elderly_profile:
        profile = ElderlyProfileResponse.model_validate(user.elderly_profile)
    elif user.user_type == "member" and user.member_profile:
        profile = MemberProfileResponse.model_validate(user.member_profile)
    elif user.user_type == "deliverer" and user.deliverer_profile:
        profile = DelivererProfileResponse.model_validate(user.deliverer_profile)
    elif user.user_type == "admin" and user.admin_profile:
        profile = AdminProfileResponse.model_validate(user.admin_profile)
    
    user_with_profile = UserWithProfile(
        id=user.id,
        username=user.username,
        user_type=user.user_type,
        status=user.status,
        created_at=user.created_at,
        updated_at=user.updated_at,
        profile=profile
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=user_with_profile
    )

@router.get("/profile", response_model=UserWithProfile)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    profile = None
    if current_user.user_type == "elderly" and current_user.elderly_profile:
        profile = ElderlyProfileResponse.model_validate(current_user.elderly_profile)
    elif current_user.user_type == "member" and current_user.member_profile:
        profile = MemberProfileResponse.model_validate(current_user.member_profile)
    elif current_user.user_type == "deliverer" and current_user.deliverer_profile:
        profile = DelivererProfileResponse.model_validate(current_user.deliverer_profile)
    elif current_user.user_type == "admin" and current_user.admin_profile:
        profile = AdminProfileResponse.model_validate(current_user.admin_profile)
    
    return UserWithProfile(
        id=current_user.id,
        username=current_user.username,
        user_type=current_user.user_type,
        status=current_user.status,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
        profile=profile
    )

@router.post("/change-password", response_model=Dict[str, str])
async def change_password(
    change_data: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    success = auth_service.change_password(
        db, current_user, change_data.old_password, change_data.new_password
    )
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Old password is incorrect"
        )
    return {"message": "Password changed successfully"}

@router.post("/register", response_model=Dict[str, Any])
async def register(
    register_data: RegisterRequest,
    db: Session = Depends(get_db)
):
    user = auth_service.register_user(
        db, 
        register_data.username, 
        register_data.password, 
        register_data.user_type,
        register_data.profile
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    return {
        "id": user.id,
        "username": user.username,
        "user_type": user.user_type,
        "status": user.status
    }

@router.put("/profile", response_model=UserWithProfile)
async def update_profile(
    profile_data: Union[ElderlyProfileUpdate, MemberProfileUpdate, DelivererProfileUpdate],
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    updated_user = user_service.update_user_profile(db, current_user, profile_data.model_dump(exclude_unset=True))
    
    profile = None
    if current_user.user_type == "elderly" and current_user.elderly_profile:
        profile = ElderlyProfileResponse.model_validate(current_user.elderly_profile)
    elif current_user.user_type == "member" and current_user.member_profile:
        profile = MemberProfileResponse.model_validate(current_user.member_profile)
    elif current_user.user_type == "deliverer" and current_user.deliverer_profile:
        profile = DelivererProfileResponse.model_validate(current_user.deliverer_profile)
    
    return UserWithProfile(
        id=updated_user.id,
        username=updated_user.username,
        user_type=updated_user.user_type,
        status=updated_user.status,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at,
        profile=profile
    )

@router.post("/logout", response_model=Dict[str, str])
async def logout(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    # 退出登录时设置配送员状态为离线
    if current_user.user_type == "deliverer" and current_user.deliverer_profile:
        current_user.deliverer_profile.status = "offline"
        db.commit()
    
    return {"message": "Logged out successfully"}

@router.post("/wechat-login", response_model=Token)
async def wechat_login(
    login_data: WechatLoginRequest,
    db: Session = Depends(get_db)
):
    try:
        user = auth_service.wechat_login(db, login_data.code, login_data.user_type)
        
        # 登录成功后设置配送员状态为在线
        if user.user_type.value == "deliverer" and user.deliverer_profile:
            user.deliverer_profile.status = "available"
            db.commit()
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id, "user_type": user.user_type},
            expires_delta=access_token_expires
        )
        
        profile = None
        if user.user_type == "elderly" and user.elderly_profile:
            profile = ElderlyProfileResponse.model_validate(user.elderly_profile)
        elif user.user_type == "member" and user.member_profile:
            profile = MemberProfileResponse.model_validate(user.member_profile)
        elif user.user_type == "deliverer" and user.deliverer_profile:
            profile = DelivererProfileResponse.model_validate(user.deliverer_profile)
        
        user_with_profile = UserWithProfile(
            id=user.id,
            username=user.username,
            user_type=user.user_type,
            status=user.status,
            created_at=user.created_at,
            updated_at=user.updated_at,
            profile=profile
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user=user_with_profile
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )