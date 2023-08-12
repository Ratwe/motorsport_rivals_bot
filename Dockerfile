FROM python:3.11 AS builder
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.11-slim
WORKDIR /code

COPY ./src .
 
ENV PATH=/root/.local:$PATH

CMD [ "python", "-u", "./main.py" ]

