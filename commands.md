## Initialize alembic sqlalchemy migrations tool
alembic init alembic

## Build fastAPI app
docker-compose build

## Run WEB application
docker-compose up

## Make migrations
docker-compose run app alembic revision --autogenerate -m "New Migration"
docker-compose run app alembic upgrade head