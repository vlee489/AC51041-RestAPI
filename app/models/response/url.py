"""url response model"""
from pydantic import BaseModel


class UrlResponse(BaseModel):
    url: str
