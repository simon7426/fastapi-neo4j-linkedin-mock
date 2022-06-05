from neo4j import GraphDatabase
from pydantic import AnyUrl

from project.config import get_settings

settings = get_settings()
uri: AnyUrl = settings.database_url
username: str = settings.database_user
password: str = settings.database_password
driver = {"driver": GraphDatabase.driver(uri=uri, auth=(username, password))}
