
import src.tokenize_str
from src.services.TransactionService import TransactionService
from src.models.neo4j_models import Transaction, NFT
from src.repository.DataRepository import DataRepository
from src.database.neo4j import Neo4jDatabase
from src.tag_types import  TransactionWithTags

#SCRIPT TO INSERT FIRST DATA FROM LOG FILE TO NEO4J
def main():
    data = DataRepository.get_instance().get_data()
    driver = Neo4jDatabase.get_instance().driver
    transaction_service = TransactionService(driver)
    counter = 0
    batchSize = input("Size of batch : ")
    batches = len(data) // int(batchSize)
    batchesCount = 1
    transactionsWithTags: list[TransactionWithTags] = []
    print('Starting...')
    for item in data:
        if(item['nft']['description']):
            result = src.tokenize_str.tokenize(item['nft']['description'])
            tags = [(tag, value) for (tag, value) in result.items()]
            
        transaction = Transaction(
            item['id'],
            item['amount'],
            item['fromAddress'],
            item['toAddress'],
        )
        
        nft = NFT(
            item['nft']['id'],
            item['nft']['name'],
            item['nft']['uri'],
            item['nft']['description'],
            str(item['nft']['attributes'])
        )
        counter += 1
        transactionsWithTags.append((transaction, (nft, tags)))
        if counter == int(batchSize):
            print(f"Sending batch {batchesCount} / {batches} ")
            transaction_service.processMultipleTransactions(transactionsWithTags)
            transactionsWithTags = []
            counter = 0
            batchesCount += 1

    if (len(transactionsWithTags) > 0):
        print(f"Sending batch {batchesCount} / {batches} ")
        transaction_service.processMultipleTransactions(transactionsWithTags)
        print("Batch sent!")
        print('Done!')