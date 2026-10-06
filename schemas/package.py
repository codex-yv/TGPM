from pydantic import BaseModel, Field, field_validator
from typing import List, Dict

class PackageSchema(BaseModel):
    package_name: str
    destination_id: List[int]
    description : str
    duration: int = Field(default=1, gt = 0, lt=30)
    price: float = Field(default=0, gt=-1, description="The price should be greater than 0.")
    category_id: List[int]
    itinerary: Dict[str, List[str]]
    inclusions: List[str]
    exclusions: List[str]
    image_id: List[int] | None = None

class CategorySchema(BaseModel):
    category: str

    @field_validator('category')
    @classmethod
    def formatted_cat(cls, value:str):
        return value.lower().strip().replace(' ', '_')



class DestinationSchema(BaseModel):
    destination_text: List[int]

