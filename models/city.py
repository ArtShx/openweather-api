from sqlalchemy import Column, Float, String, ForeignKey, Integer, DateTime, null
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.schema import PrimaryKeyConstraint

from config.database import Base


class City(Base):
    __tablename__ = "city"
    city_id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, nullable=False)
    date = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Integer)

    user_id = Column(Integer, ForeignKey("process.user_id"))
    process = relationship("Process", back_populates="cities")

    __table_args__ = (PrimaryKeyConstraint("city_id", "user_id"),)
