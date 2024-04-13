from cassandra.cluster import Cluster

cluster = Cluster(['172.19.0.2'])

cassandra_session = cluster.connect('fastapiinstagram')

