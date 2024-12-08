from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_driver():
    uri = os.getenv("NEO4J_URI")
    user = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")
    return GraphDatabase.driver(uri, auth=(user, password))
