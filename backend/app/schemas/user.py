from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    user_type: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ElderlyProfileBase(BaseModel):
    name: str
    phone: Optional[str] = None
    address: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    dietary_preferences: Optional[str] = None
    location: Optional[str] = None
    avatar: Optional[str] = None

class ElderlyProfileCreate(ElderlyProfileBase):
    pass

class ElderlyProfileResponse(ElderlyProfileBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class ElderlyProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    dietary_preferences: Optional[str] = None
    location: Optional[str] = None

class MemberProfileBase(BaseModel):
    name: str
    phone: Optional[str] = None
    avatar: Optional[str] = None

class MemberProfileCreate(MemberProfileBase):
    pass

class MemberProfileResponse(MemberProfileBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class MemberProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None

class DelivererProfileBase(BaseModel):
    name: str
    phone: Optional[str] = None
    vehicle_type: Optional[str] = None
    avatar: Optional[str] = None

class DelivererProfileCreate(DelivererProfileBase):
    pass

class DelivererProfileResponse(DelivererProfileBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DelivererProfileUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    vehicle_type: Optional[str] = None

class AdminProfileBase(BaseModel):
    name: str
    phone: Optional[str] = None

class AdminProfileCreate(AdminProfileBase):
    pass

class AdminProfileResponse(AdminProfileBase):
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserWithProfile(UserInDB):
    profile: Optional[Union[
        ElderlyProfileResponse,
        MemberProfileResponse,
        DelivererProfileResponse,
        AdminProfileResponse
    ]] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserWithProfile

class ChangePassword(BaseModel):
    old_password: str
    new_password: str

class RegisterRequest(BaseModel):
    username: str
    password: str
    user_type: str
    profile: dict

class WechatLoginRequest(BaseModel):
    code: str
    user_type: str