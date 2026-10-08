from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional

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
    category: List[str]

    @field_validator('category')
    @classmethod
    def formatted_cat(cls, value:List[str]) -> list:
        res = []
        for val in value:
            res.append(val.lower().strip().replace(' ', '_'))
        return res

class DestinationSchema(BaseModel):
    destination_text: List[str]
    
    @field_validator('destination_text')
    @classmethod
    def formatted_cat(cls, value:List[str]):
        res = []
        for val in value:
            res.append(val.lower().strip().replace(' ', '_'))
        return res

class PackageToggleSchema(BaseModel):
    package_id: int


class UpadtePackageSchema(BaseModel):
    package_id: Optional[int] = None
    package_name: Optional[str] = None
    destination_id: Optional[List[int]] = None
    description : Optional[str] = None
    duration: Optional[int]= Field(default=None, gt = 0, lt=30)
    price: Optional[float ]= Field(default=None, gt=-1, description="The price should be greater than 0.")
    category_id: Optional[List[int]] = None
    itinerary: Optional[Dict[str, List[str]]] = None
    inclusions: Optional[List[str]] = None
    exclusions: Optional[List[str]] = None
    image_id: Optional[List[int] | None] = None