FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /temp/requirements.txt
RUN pip install --no-cache -r /temp/requirements.txt

COPY . /backend

WORKDIR /backend
EXPOSE 8000

