FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml /app/
COPY . /app/

RUN uv pip compile pyproject.toml > requirements.txt

RUN uv pip install -r requirements.txt --system

COPY . .

CMD ["python", "-m", "src.app.main"]