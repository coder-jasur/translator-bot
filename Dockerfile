FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN apt-get update && apt-get install -y gcc libpq-dev build-essential && rm -rf /var/lib/apt/lists/*

RUN pip install -r <(uv export --format=requirements-txt)

COPY . .

CMD ["python", "-m", "src.app.main"]