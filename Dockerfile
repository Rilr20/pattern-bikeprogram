# 1. Base image
FROM python:3.8.3-slim-buster

WORKDIR /bikeprogram

COPY . .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir requests

CMD [ "python", "./main.py" ]