FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /app

COPY pyproject.toml uv.lock /app/

# 1. requirements.txt generatsiya qilish
RUN uv export --format=requirements-txt > /app/requirements.txt

# 2. OS-level dependencies (masalan, psycopg2 uchun)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# 3. Python dependencylarni o‘rnatish
RUN uv pip install -r /app/requirements.txt --system

COPY . .

CMD ["python", "-m", "src.app.main"]