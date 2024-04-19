from cassandra.cluster import Cluster

cluster = Cluster(['172.19.0.2'])


FILEPATH = "./images/"

cassandra_session = cluster.connect('fastapiinstagram')
