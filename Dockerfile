FROM python:3.6

ENV PYTHONUNBUFFERED 1

RUN mkdir /todoproject

WORKDIR /todoproject

ADD . /todoproject/

RUN pip install -r requirements.txt