from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..repository.process_repository import ProcessRepository
from ..repository.city_repository import CityRepository
from ..schemas.city_schema import CityCreate, CityUpdate
from ..schemas.process_schema import (
    ProcessCreateInput,
    ProcessCreateOutput,
    ProcessGetInput,
    ProcessGetOutput,
    ProcessUpdate,
    Weather,
)
from ..weather_api import OpenWeatherAPI


class ProcessService:
    def __init__(self, session: Session):
        self.process_repository = ProcessRepository(session)
        self.city_repository = CityRepository(session)

    def create(self, data: ProcessCreateInput) -> ProcessCreateOutput:
        if self.process_repository.process_exists_by_id(data.user_id):
            raise HTTPException(status_code=400, detail="Process already exists")
        process = self.process_repository.create(data)
        for city_id in data.cities_id:
            city = CityCreate(city_id=city_id, user_id=data.user_id)
            self.city_repository.create(city)

        # Add OpenWeatherAPI requests on queue
        OpenWeatherAPI.add_to_queue(data.user_id, data.cities_id)
        return process

    def get_completed_process(self, user_id) -> ProcessGetOutput:
        all_cities = self.city_repository.get_by_user_id(user_id)
        total_cities = len(all_cities)
        if total_cities == 0:
            return ProcessGetOutput(
                user_id=None, percentage=0, total_cities=0, cities=[]
            )

        total_completed = 0
        cities = []
        for city in all_cities:
            if city.temperature is not None:
                total_completed += 1
                city = city.__dict__
                cities.append(
                    Weather(
                        city_id=city["city_id"],
                        temperature=city["temperature"],
                        humidity=city["humidity"],
                        date=city["date"],
                    )
                )

        percentage = (total_completed / total_cities) * 100
        return ProcessGetOutput(
            user_id=user_id,
            percentage=percentage,
            total_cities=total_cities,
            cities=cities,
        )

    def update(self, data: ProcessUpdate) -> None:
        city_update = CityUpdate(
            user_id=data.user_id,
            city_id=data.city_id,
            temperature=data.temperature,
            humidity=data.humidity,
        )
        self.city_repository.update(city_update)
