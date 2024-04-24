#!/usr/bin/env bash

echo "Waiting for Cassandra to be available..."
until cqlsh cassandra -u cassandra -p cassandra -e "DESCRIBE KEYSPACES"
do
    echo "Cassandra is unavailable - sleeping"
    sleep 5
done

echo "Cassandra is up - executing commands"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS fastapiinstagram WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS fastapiinstagram.image (sensor_id uuid, registered_at timestamp, temperature int, PRIMARY KEY ((sensor_id), registered_at));"

echo "Keyspace and Tables created."
