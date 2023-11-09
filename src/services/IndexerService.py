import os 
import requests

class IndexerService:

    def __init__(self):
        self.indexer_uri = os.getenv("INDEXER_URI")


    def runQuery(self, query):
        raw = requests.post(self.indexer_uri+"/graphql", 
            json = query,
            headers= {
                "Content-Type": "application/json",
                "Accept": "application/json"
                }
        )

        return raw.json()

    