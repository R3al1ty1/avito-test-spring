FROM python:3.12-alpine

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml .

RUN uv pip install --system -e .

RUN uv pip install --system -e ".[tests]"

COPY . .

CMD ["python", "main.py"]