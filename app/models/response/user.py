"""user response model"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserResponse(BaseModel):
    user_id: str
    oid: str
    email: EmailStr
    first_name: str
    last_name: str
    last_login: Optional[datetime]
