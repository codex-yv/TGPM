from pydantic import BaseModel, ConfigDict, field_validator
from typing import List,Dict, Union, Tuple, Any

class PackagePostResponse(BaseModel):
    status: bool
    message: str
    data: int | None = None

class CategoryPostResponse(BaseModel):
    status: bool
    message: str
    data: List[int] | None = None

class DestinationPostResponse(BaseModel):
    status: bool
    message: str
    data: List[int] | None = None


class ToggleResponse(BaseModel):
    status: bool
    message: str
    data: bool | None = None

class PackageUpdationResponse(BaseModel):
    status: bool
    message: str
    data: Any = None

class CategoriesGetResponse(BaseModel):
    id: int
    category_text: str

    @field_validator('category_text')
    @classmethod
    def normalize_cat(cls, value:str):
        return value.title().replace('_', ' ')

    model_config = ConfigDict(from_attributes=True)

class DestinationGetResponse(BaseModel):
    id: int
    destination_text: str

    @field_validator('destination_text')
    @classmethod
    def normalize_cat(cls, value:str):
        return value.title().replace('_', ' ')

    model_config = ConfigDict(from_attributes=True)

class PackageGetResponse(BaseModel):
    id: int
    package_name: str
    destinations: List[Union[str, None]]
    description : str
    duration: int
    price: float
    categories: List[Union[str, None]]
    itinerary: Dict[str, List[str]]
    inclusions: List[Union[str, None]]
    exclusions: List[Union[str, None]]
    images: List[str]
    status: bool

    @field_validator('package_name')
    @classmethod
    def update_package_name(cls, value) -> str:
        return value.replace("_", " ").title()
    
    model_config = ConfigDict(from_attributes=True)

