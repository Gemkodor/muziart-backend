FROM python:3.12-slim

WORKDIR /app

# System deps for mysqlclient
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev

# Copy source
COPY . .

EXPOSE 8000

CMD ["sh", "-c", "uv run python manage.py collectstatic --no-input && uv run python manage.py migrate && uv run gunicorn muziart.wsgi:application --bind 0.0.0.0:8000 --workers 3"]
