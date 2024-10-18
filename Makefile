.PHONY: install run test migrate

install:
	poetry install

run:
	poetry run uvicorn real_time_chat.main:app --reload --host 0.0.0.0 --port 8000

migrate:
	poetry run alembic upgrade head

test:
	poetry run pytest

develop: clean_dev  ##@Develop Create project venv
	python3.12 -m venv .venv
	.venv/bin/pip install -U pip poetry
	.venv/bin/poetry config virtualenvs.create false
	.venv/bin/poetry install

clean_dev:
	rm -rf .venv/

clean_pycache:
	find . -type d -name __pycache__ -exec rm -rf {} \+


