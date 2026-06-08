FROM python:3.12-slim

#! Upgrading the base image for security patches and bug fixes
RUN apt-get update && apt-get install -y git && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000