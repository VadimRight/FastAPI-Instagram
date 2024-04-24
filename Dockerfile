FROM python:3.12.2

RUN mkdir /fastapi_app
WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod +x cassandra_init.sh
RUN chmod +x wait_for_cassandra.sh
RUN chmod +x start.sh

CMD ["/fastapi_app/wait_for_cassandra.sh", "-t", "30", "cassandra_instagram:9042", "--", "/fastapi_app/start.sh"]
