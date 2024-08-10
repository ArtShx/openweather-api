from routers.v1 import process
from utils.init_db import create_tables

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

router.include_router(process.router)


create_tables()
