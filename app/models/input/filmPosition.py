"""Film Position model"""
from pydantic import BaseModel


class FilmPosition(BaseModel):
    pos: float
