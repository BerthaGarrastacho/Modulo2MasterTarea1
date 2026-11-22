from pydantic import BaseModel, Field
from typing import List

# class Camera(BaseModel):
#     rating: int = Field(gt=0, le=1000000000, default="0")
#     stars: int = Field(gt=0, le=5, default="0")

class User(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=300, default="Jhon Doe")
    username: str = Field(min_length=1, max_length=100, default="@JhonDoe-PH")
    email: str = Field( min_length=6, max_length=254,pattern=r"^[\w\.-]+@[\w\.-]+\.\w{2,}$")
    # camera: Camera
    # phCategory: List[str] = Field(min_length=1)

