#!/bin/bash
# Wait until Cassandra is ready to accept connections
until printf "" 2>>/dev/null >>/dev/tcp/cassandra_instagram/9042; do 
    sleep 5;
    echo "Waiting for Cassandra...";
done

# Initialization commands
cqlsh -e "CREATE KEYSPACE IF NOT EXISTS fastapiinstagram WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 3};"
cqlsh -e "CREATE TABLE IF NOT EXISTS fastapiinstagram.image (id uuid PRIMARY KEY, item_id uuid, path varchar, user_id uuid);"

