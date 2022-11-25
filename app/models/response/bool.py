"""Simple bool response model"""
from pydantic import BaseModel


class BoolResponse(BaseModel):
    status: bool
