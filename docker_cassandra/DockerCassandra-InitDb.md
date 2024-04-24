## Initializing a Cassandra Docker container with keyspace and data

This gist shows you how to easily create a cassandra image with initial keyspace and values populated.

It is very generic: the `entrypoint.sh` is able to execute any cql file located in `/docker-entrypoint-initdb.d/`,
a bit like what you do to initialize a MySQL container.

You can add any `*.sh` or `*.cql` scripts inside `/docker-entrypoint-initdb.d`, but note that:

* `*.sh` files will be executed **BEFORE** launching cassandra
* `*.cql` files will be executed (with `cqlsh -f`) **AFTER** cassandra started

Files are executed in name order (ls * | sort)

## How to use

1. download the `Dockerfile` and `entrypoint.sh`
2. edit the `Dockerfile` in order to copy your init scripts inside `/docker-entrypoint-initdb.d/`
3. build the image: ` docker build -t my-cassandra-image .`
4. run the image: `docker run --rm -p 9042:9042 --name cassandra-container -d my-cassandra-image`

Note that the scripts in `/docker-entrypoint.sh` will only be called on startup. If you decide to persist the data using a volume, 
this will work all right: the scripts won't be executed when you boot your container a second time. By using a volumne, I mean, e.g.:

```bash
docker run --rm -d \
    -p 9042:9042 \
    -v $PWD/data:/var/lib/cassandra \
    --name cassandra-container \
    my-cassandra-image
```