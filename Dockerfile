FROM python:3.11

WORKDIR /app
COPY main.py rules.py confs.py requirements.txt lib /app

RUN pip install -r requirements.txt
