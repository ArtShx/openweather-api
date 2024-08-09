from typing import List

from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from ...config.database import get_db
from ...schemas.process_schema import (
    ProcessCreateInput,
    ProcessCreateOutput,
    ProcessGetInput,
    ProcessGetOutput,
)
from ...service.process_service import ProcessService


router = APIRouter(prefix="/process")


@router.post("", status_code=201, response_model=ProcessCreateOutput)
async def create_process(
    data: ProcessCreateInput,
    session: Session = Depends(get_db),
):
    _service = ProcessService(session)
    return _service.create(data)


@router.get("", status_code=200, response_model=ProcessGetOutput)
async def get_process(
    data: ProcessGetInput, session: Session = Depends(get_db)
) -> ProcessGetOutput:
    _service = ProcessService(session)
    return _service.get_completed_process(data.user_id)
