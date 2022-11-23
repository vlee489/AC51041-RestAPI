"""Session Login response model"""
from pydantic import BaseModel
from datetime import datetime


class LoginResponse(BaseModel):
    session_id: str
    expiry: datetime
