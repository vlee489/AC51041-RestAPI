"""Film response model"""
from pydantic import BaseModel
from typing import List


class FilmResponse(BaseModel):
    id: str
    name: str
    tags: List[str]
    categories: List[str]
    description: str
    tag_line: str
    thumbnail_url: str
