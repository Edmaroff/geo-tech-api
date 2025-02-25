FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ./src /app