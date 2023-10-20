from src.database.neo4j import Neo4jDatabase
from src.data_processing import DataProcessor
from src.logs.logger import DataProcessingLogger
import os
import requests

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

indexer_uri = os.getenv("INDEXER_URI")

raw = requests.post(indexer_uri+"/graphql", json = {
    "operationName": "getTransactions",
    "variables": None,
    "query": """query getTransactions {
                    nftTransferEntities(limit: 20) {
                        amount
                        id
                        fromAddress
                        toAddress
                        nft {
                        id
                        }
                    }
                }"""
    },
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
)

parsed = raw.json()

transfers = parsed['data']['nftTransferEntities']

for transfer in transfers:
    print(transfer)
    logger.log(transfer)
