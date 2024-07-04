FROM python:3.9

RUN python -m pip install --upgrade pip


RUN pip install poetry


WORKDIR /app

COPY pyproject.toml poetry.lock ./


RUN poetry install --no-root --no-dev

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
