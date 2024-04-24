#!/usr/bin/env bash
sleep 5

echo "Cassandra is up - executing commands"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE KEYSPACE IF NOT EXISTS fastapiinstagram WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'};"
cqlsh cassandra -u cassandra -p cassandra -e "CREATE TABLE IF NOT EXISTS fastapiinstagram.image (id uuid PRIMARY KEY, item_id uuid, path varchar, user_id uuid);"

echo "Keyspace and Tables created."
