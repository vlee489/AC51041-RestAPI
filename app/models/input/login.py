"""Session Login request model"""
from pydantic import BaseModel, Field, EmailStr


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=4)
