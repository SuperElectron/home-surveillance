FROM python:3.9.10-buster

RUN mkdir /server
WORKDIR /server
EXPOSE 5000

COPY . .

RUN pip3 install pip-tools
RUN pip-compile setup/requirements.in
RUN pip-compile setup/requirements-prod.in
RUN pip install -r setup/requirements.txt

ENTRYPOINT [ "gunicorn", "-b 0.0.0.0:5000", "-w 4", "-k uvicorn.workers.UvicornWorker", "main:app" ]