FROM python:3.11.4

WORKDIR /app

COPY . .

RUN pip install -r packages.txt

CMD uvicorn server:app --port 8001 --host 0.0.0.0