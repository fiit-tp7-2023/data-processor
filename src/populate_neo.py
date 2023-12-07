from src.services.TransactionService import TransactionService
from src.services.TokenizationService import TokenizationService
from src.models.neo4j_models import Transaction, NFT, Address
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
        from_address = Address(
            address=item["fromAddress"]["id"], 
            createdAtBlock=item["fromAddress"]["createdAtBlock"]
        )
        to_address = Address(
            address=item["toAddress"]["id"], 
            createdAtBlock=item["toAddress"]["createdAtBlock"]
        )
        transaction = Transaction(
            id=item["id"],
            amount=item["amount"],
            from_address=from_address,
            to_address=to_address,
        )

        nft = NFT(
            address=item["nft"]["id"],
            animationUrl=item["nft"]["animationUrl"],
            attributes=item["nft"]["attributes"],
            createdAtBlock=item["nft"]["createdAtBlock"],
            description=item["nft"]["description"],
            externalUrl=item["nft"]["externalUrl"],
            image=item["nft"]["image"],
            name=item["nft"]["name"],
            raw=item["nft"]["raw"],
            tokenId=item["nft"]["tokenId"],
            uri=item["nft"]["uri"],
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
