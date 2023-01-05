"""Session Signup request model"""
from pydantic import BaseModel, Field, EmailStr


class SignupCredentials(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(min_length=4)
