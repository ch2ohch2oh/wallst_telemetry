# syntax=docker/dockerfile:2

FROM python:3.8-slim-buster

WORKDIR /app

COPY . .
RUN pip install -r requirements.txt
RUN pylint .

CMD ["python3", "ingest.py"]