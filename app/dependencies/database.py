from app.db.couchdb import couch_client, CouchDBClient

def get_db_client() -> CouchDBClient:
    return couch_client