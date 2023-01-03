"""recommendation model"""
from pydantic import BaseModel
from typing import Dict


class RecommendationResponse(BaseModel):
    tags: Dict[str, int]
    categories: Dict[str, int]
