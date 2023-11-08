
import json
import src.tokenize_str
from src.services.TransactionService import TransactionService
from src.models.neo4j_models import Transaction, Tag
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
    counter = 0
    batchSize = input("Size of batch : ")
    batches = len(data) // int(batchSize)
    batchesCount = 1
    transactions = []
    print('Starting...')
    for item in data:
        if(item['nft']['description']):
            result = src.tokenize_str.tokenize(item['nft']['description'])
            tags = [(Tag(type=tag), value) for (tag, value) in result.items()]
            
            print(result)
        transaction = Transaction(
            from_address=item['fromAddress'],
            to_address=item['toAddress'],
            transaction_id=item['id'],
            amount=item['amount'],
            nft = item['nft']
        )
        counter += 1
        transactions.append(transaction)
        if counter == int(batchSize):
            print(f"Sending batch {batchesCount} / {batches} ")
            transaction_service.processMultipleTransactions(transactions)
            transactions = []
            counter = 0
            batchesCount += 1

    if (len(transactions) > 0):
        print(f"Sending batch {batchesCount} / {batches} ")
        transaction_service.processMultipleTransactions(transactions)
        print("Batch sent!")
        print('Done!')