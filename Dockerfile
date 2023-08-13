FROM python:3.11

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD [ "python", "-u", "./src/main.py" ]
