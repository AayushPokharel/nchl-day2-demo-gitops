FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY secrets secrets
COPY userdata.json userdata.json
COPY entrypoint.sh entrypoint.sh
COPY app.py app.py

RUN chmod +x entrypoint.sh


ENTRYPOINT ["./entrypoint.sh"]