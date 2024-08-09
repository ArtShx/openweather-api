from sqlalchemy.orm import Session

from datetime import datetime

from ..models.process import Process
from ..schemas.process_schema import ProcessCreateInput, ProcessCreateOutput


class ProcessRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: ProcessCreateInput) -> ProcessCreateOutput:
        parsed_data = data.model_dump(exclude_none=True)
        parsed_data["date"] = datetime.now()
        del parsed_data["cities_id"]

        process = Process(**parsed_data)
        self.session.add(process)
        self.session.commit()
        self.session.refresh(process)
        return ProcessCreateOutput(user_id=data.user_id)

    def get_by_id(self, _id: int) -> Process:
        return self.session.query(Process).filter_by(user_id=_id).first()

    def process_exists_by_id(self, _id: int) -> bool:
        process = self.get_by_id(_id)
        return process is not None
