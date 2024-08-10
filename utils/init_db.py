from config.database import engine
from models.process import Process
from models.city import City


def create_tables():
    """
    Creates all database tables defined in the application.
    """
    Process.metadata.create_all(bind=engine)
    City.metadata.create_all(bind=engine)
