import asyncio
import os

from fastapi import FastAPI

from utils import utils

env = utils.read_env("./env")
os.environ.update(env)


from config.database import get_db
from routers import api
from weather_api import OpenWeatherAPI

app = FastAPI()
app.include_router(api.router)


@app.get("/", status_code=200)
async def health_check():
    return {"health_check": "OK"}


@app.on_event("startup")
async def startup_event():
    session = next(get_db())
    asyncio.create_task(OpenWeatherAPI.start_process(session))
