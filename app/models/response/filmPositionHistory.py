"""Film Position model"""
from pydantic import BaseModel


class FilmPositionHistory(BaseModel):
    film_id: str
    pos: float
