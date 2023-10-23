import requests
import os
from src.logs.logger import DataProcessingLogger
from src.services.IndexerService import IndexerService



def main():
    service = IndexerService()

    query = {
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
        }
   
    parsed = service.runQuery(query)
    
    transfers = parsed['data']['nftTransferEntities']
    for transfer in transfers:
        DataProcessingLogger.get_instance().log(transfer)