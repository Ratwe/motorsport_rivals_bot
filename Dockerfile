FROM python:3.11

COPY . /app

RUN pip install -r /app/requirements.txt

WORKDIR /app/src

ENV PYTHONPATH "${PYTHONPATH}:/app"

CMD [ "python", "-u", "main.py" ]
