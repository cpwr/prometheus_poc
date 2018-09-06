FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV LC_ALL=""
ENV LC_NAME="uk_UA.UTF-8"

RUN mkdir /src
WORKDIR /src

ADD requirements.txt .

RUN pip install -U pip && \
    pip install -r requirements.txt && \
    pip install --upgrade https://github.com/vbilyi/prometheus_toolbox/tarball/master
