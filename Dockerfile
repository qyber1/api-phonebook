FROM python:3.10-alpine

RUN apk add --no-cache build-base libffi-dev
RUN mkdir /web
COPY . /web
WORKDIR /web

RUN pip install --upgrade pip
RUN pip3 install wheel
RUN pip install -r requirements.txt
ENTRYPOINT uvicorn --factory --host 0.0.0.0 --port 8888 app.main:create_app

