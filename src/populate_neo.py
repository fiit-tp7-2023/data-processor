
import json
import os
from src.services.TransactionService import TransactionService
from src.models.neo4j_models import Transaction
from src.logs.logger import DataProcessingLogger
from dotenv import load_dotenv


#SCRIPT TO INSERT FIRST DATA FROM LOG FILE TO NEO4J
def main():
    indexer_log = DataProcessingLogger.get_instance().log_file
    data = []
    with open(indexer_log, 'r') as file:
        for line in file:
            data.append(json.loads(line))

    load_dotenv()
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    transaction_service = TransactionService(neo4j_uri, neo4j_user, neo4j_password)


    total_items = len(data)
    processed_items = 0
    for item in data:
        transaction = Transaction(
            from_address=item['fromAddress'],
            to_address=item['toAddress'],
            transaction_id=item['id'],
            nft=item['nft']['id']
        )
        transaction_service.processTransaction(transaction)
        transaction_service.processTransaction(transaction)
    
   
        processed_items += 1
        percentage = (processed_items / total_items) * 100
        print(f"Processing: {processed_items}/{total_items} ({percentage:.2f}%)", end='\r')