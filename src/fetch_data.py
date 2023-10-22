import requests
import os
from src.logs.logger import DataProcessingLogger




def main():
    logger = DataProcessingLogger("src/logs/indexer_data/indexer.log")

    indexer_uri = os.getenv("INDEXER_URI")
    raw = requests.post(indexer_uri+"/graphql", json = {
        "operationName": "getTransactions",
        "variables": None,
        "query": """query getTransactions {
                        nftTransferEntities(limit: 100) {
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
    logger.clear()
    for transfer in transfers:
        logger.log(transfer)