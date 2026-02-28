from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    is_deleted: bool = False

class UserCreate(UserBase):
    pass

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WatermarkRead(BaseModel):
    consumer_id: str
    last_exported_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ExportResponse(BaseModel):
    status: str
    consumer_id: str
    file: str
    path: str