FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
ENV PYTHONPATH=/app/src
EXPOSE 8000

CMD ["uvicorn", "swasthbot.app:app", "--host", "0.0.0.0", "--port", "8000"]
