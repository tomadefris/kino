FROM python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt /app


RUN python3 -m pip install --upgrade pip \
	&& python3 -m pip install --requirement requirements.txt

COPY app.py /app

ENV FLASK_APP=app.py

CMD ["flask","run"]
