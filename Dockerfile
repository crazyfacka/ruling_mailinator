FROM python:3.11

WORKDIR /app
COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY main.py rules.py confs.py /app
COPY lib /app/lib

ENTRYPOINT ["python", "main.py"]
