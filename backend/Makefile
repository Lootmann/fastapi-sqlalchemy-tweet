OPTION = PYTHONDONTWRITEBYTECODE=1

run:
	$(OPTION) python3 -m uvicorn api.main:app --reload

test:
	$(OPTION) python3 -m pytest -svv

cov:
	$(OPTION) python3 -m pytest --cov --cov-report=html

measure:
	$(OPTION) python3 -m pytest --durations=0 -vv

profile:
	$(OPTION) python3 -m pytest --profile-svg

migrate:
	$(OPTION) python3 -m api.migrate_db

docs:
	google-chrome http://127.0.0.1:8000/docs

req:
	pip freeze > requirements.txt

pre:
	pre-commit run --all-files
