.PHONY: install build contract start-db start test lint

install:
	uv sync && npm ci

build:
	rm -rf public/assets public/index.html
	cp -R node_modules/@hexlet/python-flight-booking-frontend/dist/. public/

contract:
	npx tsp compile contract

start-db:
	uv run app/init_db.py
	uv run app/seed_data.py

start:
	uv run app/init_db.py
	uv run app/seed_data.py
	uv run uvicorn --factory app.main:create_app --host 0.0.0.0 --port $${PORT:-8080}

test:
	uv run python -m pytest

lint:
	uv run ruff check && uv run mypy .
