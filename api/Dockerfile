FROM python:3.8

LABEL MAINTAINER Robert Lynch "rob@rlyn.ch"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD api/requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt
COPY api/ / 
WORKDIR /
CMD python3 -u app.py