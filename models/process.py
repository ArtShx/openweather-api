from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import relationship

from config.database import Base


class Process(Base):
    __tablename__ = "process"
    user_id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    cities = relationship("City", back_populates="process")
