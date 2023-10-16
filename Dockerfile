FROM python:3.10

RUN mkdir "/fastapi_app"

WORKDIR /fastapi_app

ENV PYTHONPATH=/fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
