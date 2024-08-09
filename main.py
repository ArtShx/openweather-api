import asyncio

from fastapi import FastAPI

from .routers import api
from .weather_api import OpenWeatherAPI

app = FastAPI()
app.include_router(api.router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(OpenWeatherAPI.start_process())
