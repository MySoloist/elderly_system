from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class HealthTagBase(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None

class HealthTagCreate(HealthTagBase):
    pass

class HealthTagUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

class HealthTag(HealthTagBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
