run:
	docker compose up -d

build:
	docker compose build

buildup:
	docker compose up --build

down:
	docker compose down -v

logs:
	docker compose logs -ft

restart:
	docker compose restart

migrate:
	docker compose exec app python3 -m api.migrate_db

login-app:
	docker exec -it fastapi-container /bin/bash

login-db:
	docker exec -it fastapi-postgre psql -U postgres

# tests
test:
	docker compose exec app python3.10 -m pytest -svv

re:
	docker compose exec app python3.10 -m pytest -svv --lf

# preformance
measure:
	docker compose exec app python3.10 -m pytest --durations=0

cov:
	docker compose exec app python3.10 -m pytest --cov --cov-report=html

report:
	google-chrome ./backend/htmlcov/index.html

profile:
	docker compose exec app python3.10 -m pytest --profile-svg
