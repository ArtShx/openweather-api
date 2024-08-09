from datetime import datetime
import os
from typing import List
import asyncio
from collections import deque

import aiohttp

from .repository.city_repository import CityRepository
from .schemas.city_schema import CityUpdate
from .config.database import get_db

# from .service.process_service import ProcessService
from .schemas.process_schema import ProcessUpdate, Weather

if "OPENWEATHER_KEY" not in os.environ:
    print("Failed to read OpenWeather API Key from env file")
    import sys

    sys.exit(-1)

OPENWEATHER_KEY = os.environ["OPENWEATHER_KEY"]


class OpenWeatherAPI:
    uri: str = "http://api.openweathermap.org/data/2.5/weather"
    semaphore = asyncio.Semaphore(60)
    queue = deque()

    @classmethod
    async def get(cls, city_id: int) -> Weather:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                cls.uri,
                params={"id": city_id, "appid": OPENWEATHER_KEY, "units": "metric"},
            ) as response:

                if response.status == 200:
                    payload = await response.json()
                    return Weather(
                        city_id=city_id,
                        temperature=payload["main"]["temp"],
                        humidity=payload["main"]["humidity"],
                        date=datetime.fromtimestamp(payload["dt"]),
                    )
                raise Exception("Uncaught exception, status:", response.status)

    @classmethod
    async def start_process(cls) -> List[Weather]:
        """
        Process Weather requests.
        This function manages the OpenWeatherAPI request limit.
        """
        # TODO: not ideal to use Repository objects directly
        session = next(get_db())
        city_repo = CityRepository(session)
        while True:
            if cls.queue:
                async with cls.semaphore:
                    # Get the next request from the queue
                    user_id, city_id = cls.queue.popleft()
                    print(f"Processing City: {city_id}")

                    # TODO: do not make more than 1 request for the same city in a small timespan
                    # in this case maybe just replicate the weather info
                    response = await OpenWeatherAPI.get(city_id)
                    city_repo.update(
                        CityUpdate(
                            user_id=user_id,
                            city_id=city_id,
                            temperature=response.temperature,
                            humidity=response.humidity,
                        )
                    )

                await asyncio.sleep(1)
            await asyncio.sleep(0.5)

    @classmethod
    def add_to_queue(cls, user_id: int, cities_id: List[int]) -> None:
        cls.queue.extend([(user_id, city_id) for city_id in cities_id])
