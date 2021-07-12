FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /bot

COPY requirements.txt /bot


RUN apt-get update && apt --yes install build-essential libssl-dev libffi-dev python-dev zbar-tools


RUN pip3 install -r requirements.txt --no-cache-dir

COPY . /bot

CMD ["python3","handlers.py"]
