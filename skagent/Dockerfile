FROM python:3.13.3

RUN apt-get update && \
    apt-get install -y docker.io curl gnupg2 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./skagent /app/skagent
COPY ./mcpserver /app/mcpserver
COPY ./.env /app/skagent/.env

RUN pip install --upgrade pip && \
pip install -r skagent/requirements.txt



EXPOSE 8000

CMD ["uvicorn", "skagent.main:app", "--host", "0.0.0.0", "--port", "8000"]
