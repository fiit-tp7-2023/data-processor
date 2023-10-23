import os 
from src.logs.logger import DataProcessingLogger
import requests

class IndexerService:

    def __init__(self):
        self.indexer_uri = os.getenv("INDEXER_URI")
        self.logger = DataProcessingLogger.get_instance()
        self.logger.clear()


    def runQuery(self, query, headers):
        raw = requests.post(self.indexer_uri+"/graphql", json = query,
            headers=headers)

        return raw.json()

    