import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from config.database import Base, get_db

from sqlalchemy_utils import database_exists, create_database, drop_database

from main import app
from utils.init_db import create_tables


DATABASE_URL = "postgresql://root:secret@postgres/test_db.db"

engine = create_engine(
    DATABASE_URL,
    poolclass=StaticPool,
)

if database_exists(engine.url):
    drop_database(engine.url)

create_database(engine.url)
engine.connect()


# Create a sessionmaker to manage sessions
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables in the database
Base.metadata.create_all(bind=engine)
# create_tables()


@pytest.fixture(scope="function")
def db_session():
    """
    Create a new database session with a rollback at the end of the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Create a test client that uses the override_get_db fixture to return a session.
    """

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
