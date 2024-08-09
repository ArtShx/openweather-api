from datetime import datetime
from pydantic import BaseModel, UUID4, Field
from typing import List, Union


class Weather(BaseModel):
    city_id: int
    temperature: float
    humidity: int
    date: datetime


class ProcessWeather(BaseModel):
    user_id: int
    total_cities: int
    percentage: float
    cities: List[Weather]


class ProcessCreateInput(BaseModel):
    user_id: int
    cities_id: List[int]


class ProcessCreateOutput(BaseModel):
    user_id: int


class ProcessGetInput(BaseModel):
    user_id: int


class ProcessGetOutput(BaseModel):
    user_id: Union[int, None]
    total_cities: int
    percentage: float
    cities: List[Weather]


class ProcessUpdate(BaseModel):
    user_id: int
    city_id: int
    temperature: Union[float, None]
    humidity: Union[int, None]
