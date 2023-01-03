"""recommendation model"""
from pydantic import BaseModel
from typing import List


class Recommendation(BaseModel):
    tags: List[str]
    categories: List[str]
