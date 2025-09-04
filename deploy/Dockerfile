FROM python:3.9-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-dev

COPY semantic_layer ./semantic_layer

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "semantic_layer.api.main:app", "--host", "0.0.0.0"]
