import asyncio
from datetime import datetime, timedelta
import time

import pytest

from repository.city_repository import CityRepository
from schemas.process_schema import ProcessCreateInput
from service.process_service import ProcessService
from weather_api import OpenWeatherAPI


@pytest.mark.asyncio
async def test_weather_api(db_session):
    weather = await OpenWeatherAPI.get(3439781)
    assert weather.city_id == 3439781
    assert weather.date - datetime.now() < timedelta(seconds=1)
    assert isinstance(weather.temperature, float)
    assert isinstance(weather.humidity, int)

    # Starting background
    task = asyncio.create_task(OpenWeatherAPI.start_process(db_session))

    new_process = ProcessCreateInput(user_id=5, cities_id=[3442098, 3442778, 3443341])

    proc_svc = ProcessService(db_session)
    assert proc_svc.create(new_process)

    city_repo = CityRepository(db_session)
    for city_id in new_process.cities_id:
        created_proc = city_repo.get_by_id(new_process.user_id, city_id).__dict__
        assert created_proc["user_id"] == new_process.user_id
        assert isinstance(created_proc["create_date"], datetime)

    # Waiting for OpenWeather request completion
    finished = False
    elapsed_time = 0
    start_time = time.time()
    max_exceeded_time = 5

    while not finished and elapsed_time < max_exceeded_time:
        completed = proc_svc.get_completed_process(new_process.user_id)
        assert completed.total_cities == len(new_process.cities_id)
        finished = completed.percentage == 100
        elapsed_time = time.time() - start_time
        await asyncio.sleep(0.2)

    total_elapsed_time = time.time() - start_time
    # also not too slow
    assert total_elapsed_time < max_exceeded_time

    # stopping task
    task.cancel()

    completed = proc_svc.get_completed_process(new_process.user_id)
    assert completed.percentage == 100
    assert len(completed.cities) == len(new_process.cities_id)
    assert len(completed.cities) == completed.total_cities

    weather = completed.cities[0]
    assert weather.date - datetime.now() < timedelta(seconds=6)
    assert isinstance(weather.temperature, float)
    assert isinstance(weather.humidity, int)
