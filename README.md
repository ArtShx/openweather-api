# OpenWeather API
This projects is a web server providing 2 endpoints that collects data from OpenWeather API and stores it on Postgres.

## Setup
```
git clone https://github.com/ArtShx/openweather-api & cd openweather-api
# edit the env file by setting up you key of  OpenWeather API
docker compose up --build
```


## Endpoints
Once the application is up, check the docs and available endpoints at `http://0.0.0.0:8000/docs`

- Health Check: `http://0.0.0.0:8000/`
- Get:  `http://0.0.0.0:8000/api/v1/process?user_id={x}`
- Post: `http://0.0.0.0:8000/api/v1/process`
    Example request body schema: 
    ```
    {
	    "user_id": 1,
	    "cities_id": [3439525]
    }
    ```

### Running tests
` docker compose run api sh ./run_tests.sh `

## Tools
- Python 3.9;
- Docker / Docker compose (Container);
- Postgres (Data Persistence);
- FastAPI (Web Framework supporting HTTP protocol);
- SQLAlchemy for Database integration;


## Code Architecture
### Model
Represents the database relationship entities.

### Repository
Manages the underlying data storage and provides an interface for interacting with it.

### Service
Intermediary between the API endpoints and the repository layer. It’s responsible for implementing business logic, orchestrating interactions between different repositories, and performing necessary validations or additional operations.

### Routers
API endpoints using FastAPI routers.
