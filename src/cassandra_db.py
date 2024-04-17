from cassandra.cluster import Cluster

cluster = Cluster(['172.19.0.2'])


FILEPATH = "./images/"

cassandra_session = cluster.connect()
select_path_statement_by_item_id = cassandra_session.prepare(f"SELECT path FROM fastapiinstagram.image WHERE item_id = ? ALLOW FILTERING;")
select_path_statement_by_user_id = cassandra_session.prepare(f"SELECT path FROM fastapiinstagram.image WHERE user_id = ?  ALLOW FILTERING ;")
delete_image_statement_by_id = cassandra_session.prepare(f"DELETE FROM fastapiinstagram.image WHERE id = ? ;")
select_id_statement_by_item_id = cassandra_session.prepare(f"SELECT id FROM fastapiinstagram.image WHERE item_id = ? ALLOW FILTERING;")
