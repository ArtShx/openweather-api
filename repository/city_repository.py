from datetime import datetime
from sqlalchemy.orm import Session
from typing import List

from ..models.city import City
from ..schemas.city_schema import CityCreate, CityUpdate


class CityRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: CityCreate) -> bool:
        parsed_data = data.model_dump(exclude_none=True)
        parsed_data["date"] = datetime.now()
        city = City(**parsed_data)
        self.session.add(city)
        self.session.commit()
        self.session.refresh(city)
        return True

    def get_by_id(self, user_id: int, city_id: int) -> City:
        return (
            self.session.query(City).filter_by(user_id=user_id, city_id=city_id).first()
        )

    def get_by_user_id(self, _id: int) -> List[City]:
        return self.session.query(City).filter_by(user_id=_id).all()

    def update(self, data: CityUpdate) -> CityUpdate:
        city = self.get_by_id(user_id=data.user_id, city_id=data.city_id)
        city.temperature = data.temperature
        city.humidity = data.humidity
        self.session.commit()
        self.session.refresh(city)
        return CityUpdate(**city.__dict__)
