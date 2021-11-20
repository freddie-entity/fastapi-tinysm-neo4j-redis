from neo4j import GraphDatabase
from config import settings

def get_db():
    session = get_session()
    try:
        yield session()
    finally:
        session().close()

def get_session(db_type='write'):
	driver = GraphDatabase.driver(settings.DB_NEO4J_HOST, auth=(settings.DB_NEO4J_USERNAME,settings.DB_NEO4J_PASSWORD))
	return driver.session



