FROM python:3-alpine

WORKDIR /web
WORKDIR /web/api
COPY . .
WORKDIR /web/data
COPY ../data/rimes.db rimes.db

RUN pip install fastapi uvicorn starlette sqlite3
EXPOSE 8000

CMD ["python3", "serve.py"]
