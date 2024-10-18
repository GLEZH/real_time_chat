FROM python:3.12-slim

WORKDIR /real_time_chat

COPY pyproject.toml poetry.lock /real_time_chat/

RUN pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /real_time_chat

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "real_time_chat.main:app", "--host", "0.0.0.0", "--port", "8000"]
