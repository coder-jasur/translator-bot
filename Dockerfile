FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY uv.lock /app/

RUN uv export --format=requirements-txt > /app/requirements.txt

RUN uv pip install -r /app/requirements.txt --system

COPY . .

CMD ["python", "-m", "src.app.main"]