from repository.city_repository import CityRepository
from repository.process_repository import ProcessRepository
from schemas.city_schema import CityCreate, CityUpdate
from schemas.process_schema import ProcessCreateInput


def test_repository(db_session):
    process_repo = ProcessRepository(db_session)

    # id does not exists
    user_id = 2
    process = process_repo.get_by_id(user_id)
    assert process is None

    process_repo.create(
        ProcessCreateInput(user_id=user_id, cities_id=[3439525, 3439781])
    )

    assert process_repo.process_exists_by_id(user_id)

    city_repo = CityRepository(db_session)
    city_test = CityCreate(user_id=user_id, city_id=4)

    # does not exists
    city = city_repo.get_by_id(city_test.user_id, city_test.city_id)
    assert city is None

    city = city_repo.get_by_user_id(city_test.user_id)
    assert city == []

    city_repo.create(city_test)

    city = city_repo.get_by_id(city_test.user_id, city_test.city_id).__dict__
    assert city["city_id"] == city_test.city_id
    assert city["user_id"] == city_test.user_id

    cities = city_repo.get_by_user_id(city_test.user_id)
    assert len(cities) == 1
    new_city = cities[0].__dict__
    assert new_city["city_id"] == city_test.city_id
    assert new_city["user_id"] == city_test.user_id
    assert "temperature" in new_city
    assert "humidity" in new_city

    # Update
    city_repo.update(
        CityUpdate(
            user_id=user_id, city_id=city_test.city_id, temperature=20.123, humidity=99
        )
    )

    new_city = city_repo.get_by_id(city_test.user_id, city_test.city_id).__dict__
    assert new_city["temperature"] == 20.123
    assert new_city["humidity"] == 99
