#FROM python:3.9-slim-buster
#FROM ubuntu:18.04
FROM python:3.9-slim
ARG GIT_COMMIT
ENV GIT_COMMIT=$GIT_COMMIT



RUN mkdir /app
RUN mkdir /app/flaskapp
COPY flaskapp /app/flaskapp

COPY requirements.txt /app
COPY run.py /app



WORKDIR /app
RUN pip install -r requirements.txt


EXPOSE 5000
CMD python run.py
