from src.services.IndexerService import IndexerService
from src.services.TransactionService import TransactionService
from src.services.TokenizationService import TokenizationService
from src.database.neo4j import Neo4jDatabase
from src.repository.DataRepository import DataRepository
from src.tag_types import NftWithTags, TagWithValue
import time


def process_data(start_block, block_count, tx_limit):
    indexer_service = IndexerService()
    tokenization_service = TokenizationService()
    transaction_service = TransactionService(Neo4jDatabase.get_instance().driver)
    repo = DataRepository.get_instance()

    repo.clear()

    while True:
        transfers = indexer_service.fetch_transfers(
            start_block, start_block + block_count, 0, tx_limit
        )
        print(f"Transfers: {len(transfers)}")

        if len(transfers) == 0:
            start_block += block_count
            continue

        repo.save(transfers)
        total_start = time.time()
        print(f"Blocks: {start_block} - {start_block + block_count}")

        process_users(
            start_block, block_count, tx_limit, indexer_service, transaction_service
        )
        process_tokens(
            start_block,
            block_count,
            tx_limit,
            indexer_service,
            tokenization_service,
            transaction_service,
        )

        process_transfers(
            repo,
            indexer_service,
            transaction_service,
            start_block,
            block_count,
            tx_limit,
        )

        start_block += block_count
        total_end = time.time()
        print(f"Finished processing in {total_end - total_start} seconds")


def process_users(
    start_block, block_count, tx_limit, indexer_service, transaction_service
):
    print("Fetching users...")
    offset_users = 0
    while True:
        users = indexer_service.fetch_users(
            start_block, start_block + block_count, offset_users, tx_limit
        )
        if len(users) == 0:
            break
        transaction_service.insert_addresses(users)
        offset_users += tx_limit
    print("Users inserted successfully")


def process_tokens(
    start_block,
    block_count,
    tx_limit,
    indexer_service,
    tokenization_service,
    transaction_service,
):
    print("Fetching tokens...")
    offset_tokens = 0
    while True:
        nfts = indexer_service.fetch_tokens(
            start_block, start_block + block_count, offset_tokens, tx_limit
        )
        if len(nfts) == 0:
            break

        processed_nfts: list[NftWithTags] = []
        print(f"Tokenizing batch of {len(nfts)} nfts...")
        for nft in nfts:
            tags: list[TagWithValue] = [
                (tag, value)
                for (tag, value) in tokenization_service.tokenize(nft).items()
            ]
            processed_nfts.append((nft, tags))
        transaction_service.insert_nfts(processed_nfts)
        offset_tokens += tx_limit
    print("Tokens inserted successfully")


def process_transfers(
    repo, indexer_service, transaction_service, start_block, block_count, tx_limit
):
    print("Processing transfers...")
    offset = 0
    while repo.has_transfers():
        transaction_service.populate_db()
        repo.clear()
        offset += tx_limit
        repo.save(
            indexer_service.fetch_transfers(
                start_block, start_block + block_count, offset, tx_limit
            )
        )


def main():
    start_raw = input("Start block (12337801): ")
    start_block = 12337801 if start_raw == "" else int(start_raw)
    block_count = int(input("Block batch count: "))
    tx_limit = int(input("Transaction batch count: "))

    process_data(start_block, block_count, tx_limit)


def main_server():
    process_data(12337801, 100, 100)
