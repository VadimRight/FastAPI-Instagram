FROM python:3.12.2

WORKDIR /FastAPIApp

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY . .

CMD uvicorn src.main:app --reload
