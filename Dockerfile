FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app

COPY pyproject.toml uv.lock /app/

RUN uv export --format=requirements-txt > /app/requirements.txt

RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN uv pip install -r /app/requirements.txt --system

COPY . .

CMD ["python", "-m", "src.app.main"]