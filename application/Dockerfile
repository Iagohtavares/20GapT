FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ../application/requirements.txt /requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app