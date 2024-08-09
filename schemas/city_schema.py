from pydantic import BaseModel, UUID4, Field


class CityCreate(BaseModel):
    user_id: int
    city_id: int


class CityUpdate(BaseModel):
    user_id: int
    city_id: int
    temperature: float
    humidity: int
