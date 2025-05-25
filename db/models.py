from pydantic import BaseModel
from typing import Optional, List

class User(BaseModel):
    email: str
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str

class Coords(BaseModel):
    latitude: float
    longitude: float
    height: int

class Level(BaseModel):
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None

class Image(BaseModel):
    data: str
    title: str

class PassData(BaseModel):
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: Optional[str] = None
    user: User
    coords: Coords
    level: Level
    images: Optional[List[Image]] = None