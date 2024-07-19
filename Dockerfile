FROM python:3.9


RUN pip install poetry

RUN poetry config virtualenvs.create false

ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /fastapi_app

COPY pyproject.toml poetry.lock ./


RUN poetry install --no-root
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]