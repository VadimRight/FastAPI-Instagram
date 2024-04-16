from cassandra.cluster import Cluster

cluster = Cluster(['172.19.0.2'])


FILEPATH = "./images/"

cassandra_session = cluster.connect()
select_path_statement_by_image_id = cassandra_session.prepare(f"SELECT path FROM fastapiinstagram.image WHERE item_id = ? ALLOW FILTERING;")
select_path_statement_by_user_id = cassandra_session.prepare(f"SELECT path FROM fastapiinstagram.image WHERE user_id = ?  ALLOW FILTERING ;")
