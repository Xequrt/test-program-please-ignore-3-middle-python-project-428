.PHONY: install build start test

install:
	uv sync && npm ci

build:
	rm -rf public/assets public/index.html
	cp -R node_modules/@hexlet/python-flight-booking-frontend/dist/. public/

start:
	uv run uvicorn --factory app.main:create_app --host 0.0.0.0 --port $${PORT:-8080}

test:
	uv run python -m pytest
