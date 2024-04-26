FROM python:3.12.2

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip

RUN chmod +x *.sh
