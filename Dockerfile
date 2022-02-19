FROM python:3.9-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "gunicorn", "app:app", "-w", "3", "-b", "0.0.0.0:8000" ]