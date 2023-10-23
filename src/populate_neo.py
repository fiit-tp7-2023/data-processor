
import json
import os
from src.services.TransactionService import TransactionService
from src.models.neo4j_models import Transaction
from src.logs.logger import DataProcessingLogger
from src.database.neo4j import Neo4jDatabase


#SCRIPT TO INSERT FIRST DATA FROM LOG FILE TO NEO4J
def main():
    indexer_log = DataProcessingLogger.get_instance().log_file
    data = []
    with open(indexer_log, 'r') as file:
        for line in file:
            data.append(json.loads(line))


    driver = Neo4jDatabase.get_instance().driver
    transaction_service = TransactionService(driver)

    transactions = []
    print('Starting...')
    for item in data:
        transaction = Transaction(
            from_address=item['fromAddress'],
            to_address=item['toAddress'],
            transaction_id=item['id'],
            nft=item['nft']['id']
        )
        transactions.append(transaction)
        
    transaction_service.processMultipleTransactions(transactions)
    print('Done!')