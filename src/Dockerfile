FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .

RUN uv pip install --no-cache-dir --system -e .

RUN uv pip install --no-cache-dir --system -e ".[tests]"

COPY . .

EXPOSE 8000 9000

CMD ["python", "main.py"]