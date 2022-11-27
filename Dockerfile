FROM python:3.11.0-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat

RUN apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip

COPY . /usr/src/app/

EXPOSE 8000

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app", "--timeout", "10"]