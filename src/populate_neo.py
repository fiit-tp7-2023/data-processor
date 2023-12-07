from src.services.TransactionService import TransactionService
from src.services.TokenizationService import TokenizationService
from src.models.neo4j_models import Transaction, NFT
from src.repository.DataRepository import DataRepository
from src.database.neo4j import Neo4jDatabase
from src.tag_types import TransactionWithTags
import time


# SCRIPT TO INSERT FIRST DATA FROM LOG FILE TO NEO4J
def main():
    data = DataRepository.get_instance().get_data()
    driver = Neo4jDatabase.get_instance().driver
    transaction_service = TransactionService(driver)
    tokenization_service = TokenizationService()
    counter = 0
    batchSize = 1000
    batches = len(data) // int(batchSize)
    batchesCount = 1
    transactionsWithTags: list[TransactionWithTags] = []
    start_time = time.time()
    print("Starting...", len(data))
    for item in data:
        transaction = Transaction(
            item["id"],
            item["amount"],
            item["fromAddress"]["id"],
            item["toAddress"]["id"],
        )

        nft = NFT(
            item["nft"]["id"],
            item["nft"]["name"],
            item["nft"]["uri"],
            item["nft"]["description"],
            item["nft"]["attributes"],
        )
        result = tokenization_service.tokenize(nft)
        tags = [(tag, value) for (tag, value) in result.items()]

        counter += 1
        transactionsWithTags.append((transaction, (nft, tags)))
        if counter == batchSize:
            print(f"Sending batch {batchesCount} / {batches} ")
            transaction_service.processMultipleTransactions(transactionsWithTags)
            end_time = time.time()
            print(
                f"Processed {batchesCount} / {len(data)} in {end_time - start_time} seconds"
            )
            transactionsWithTags = []
            counter = 0
            batchesCount += 1
            start_time = time.time()

    if len(transactionsWithTags) > 0:
        print(f"Sending batch {batchesCount} / {batches} ")
        transaction_service.processMultipleTransactions(transactionsWithTags)
        print("Batch sent!")
        end_time = time.time()
        print(f"Processed {counter} / {len(data)} in {end_time - start_time} seconds")
        print("Done!")
