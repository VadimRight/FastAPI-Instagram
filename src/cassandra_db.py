from cassandra.cluster import Cluster
from src.config import CASSANDRA_HOST

cluster = Cluster([CASSANDRA_HOST])

FILEPATH = "./images/"

cassandra_session = cluster.connect('fastapiinstagram')
