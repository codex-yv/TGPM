from pydantic import BaseModel, Field
from typing import List, Dict

class PackageSchema(BaseModel):
    package_name: str
    destination: str
    description : str
    duration: int = Field(default=1, gt = 0, lt=30)
    price: float = Field(default=0, gt=-1, description="The price should be greater than 0.")
    category_id: List[int]
    itinerary =  Dict[str, List[str]]
    inclusions: List[str]
    exclusions =  List[str]
    image_id: List[str] | None = None
    status: bool

class CategorySchema(BaseModel):
    categories = List[str]