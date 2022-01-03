FROM python:3.8-slim-buster
MAINTAINER Soufiane chalouh (soufianechalouh@gmail.com)

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get -y install gcc libpq-dev python-dev

COPY ./requirements.txt /requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir /app
WORKDIR /app
COPY  ./app /app
