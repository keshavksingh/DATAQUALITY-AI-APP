FROM python:3.13.3

WORKDIR /app

COPY ./mcpserver /app/mcpserver
COPY ./.env /app/mcpserver/.env
COPY ./.env /mcpserver/.env

RUN pip install --upgrade pip && \
    pip install -r mcpserver/requirements.txt

ENTRYPOINT ["python", "mcpserver/server.py"]
