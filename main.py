from src.database.neo4j import Neo4jDatabase
from src.data_processing import DataProcessor
from src.logs.logger import DataProcessingLogger
import os

from dotenv import load_dotenv


#load environment variables from .env file
load_dotenv()
neo4j_uri = os.getenv("NEO4J_URI")
neo4j_user = os.getenv("NEO4J_USER")
neo4j_password = os.getenv("NEO4J_PASSWORD")

# Initialize and connect to Neo4j
neo4j = Neo4jDatabase(neo4j_uri, neo4j_user, neo4j_password)
neo4j.print_greeting("hello, world")


# Initialize data processor
data_processor = DataProcessor()

# Initialize logger
logger = DataProcessingLogger("logs/data_processing.log")