-- Here, you can execute any CQL commands, e.g.

CREATE KEYSPACE fastapiinstagram WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1};

CREATE TABLE some_keyspace.some_table (
    id uuid PRIMARY KEY,
    item_id uuid,
    path varchar,
    user_id uuid,
    )
