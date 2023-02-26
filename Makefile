run:
	docker compose up -d

build:
	docker compose build

buildup:
	docker compose up --build

# -v means remove all volumes attached
down:
	docker compose down -v

logs:
	docker compose logs -ft

restart:
	docker compose restart

# tests
test:
	docker compose exec app python3.10 -m pytest -svv

measure:
	docker compose exec app python3.10 -m pytest --durations=0

# preformance
cov:
	docker compose exec app python3.10 -m pytest --cov --cov-report=html

profile:
	docker compose exec app python3.10 -m pytest --profile-svg
