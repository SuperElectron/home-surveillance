FROM python:3.9.10-buster

RUN mkdir /server
WORKDIR /server
EXPOSE 5000

COPY main.py .
COPY requirements-prod.txt .
COPY .env.example ./.env

COPY app/ ./app
RUN pip install -r requirements-prod.txt

ENTRYPOINT [ "gunicorn", "-b 0.0.0.0:5000", "-w 4", "-k uvicorn.workers.UvicornWorker", "main:app" ]