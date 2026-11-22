from pydantic import BaseModel, Field
from typing import List

class Games(BaseModel):
    id: int
    name: str
    
class Genre(BaseModel):
    genre: str
    games: List[Games]
   

