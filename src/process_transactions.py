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

        if len(transfers) == 0:
            print("\n\n")
            print("_" * 50)
            print(f"Processing {block_count} blocks")
            print(
                f"\nBlocks:                                 {start_block} - {start_block + block_count}"
            )
            print("Nothing to process")
            print("¯" * 50)
            start_block += block_count
            continue

        repo.save(transfers)
        total_start = time.time()
        print("\n\n")
        print("_" * 50)
        print(f"Processing {block_count} blocks")
        print(
            f"\nBlocks:                                 {start_block} - {start_block + block_count}"
        )

        # Add new addresses that were created in this block range
        process_users(
            start_block, block_count, tx_limit, indexer_service, transaction_service
        )

        # Add new Tokens that were created in this block range
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
        total_time = "{:.2f}".format(total_end - total_start)
        print(
            f"\nFinished processing {block_count} blocks  in            {total_time} seconds"
        )
        print("¯" * 50)


def process_users(
    start_block, block_count, tx_limit, indexer_service, transaction_service
):
    offset_users = 0
    totalUsers = 0
    while True:
        users = indexer_service.fetch_users(
            start_block, start_block + block_count, offset_users, tx_limit
        )
        totalUsers += len(users)
        if len(users) == 0:
            break
        transaction_service.insert_addresses(users)
        offset_users += tx_limit

    print(f"Unique users processed:                         {totalUsers}")


def process_tokens(
    start_block,
    block_count,
    tx_limit,
    indexer_service,
    tokenization_service,
    transaction_service,
):
    offset_tokens = 0
    total_nfts = 0
    while True:
        nfts = indexer_service.fetch_tokens(
            start_block, start_block + block_count, offset_tokens, tx_limit
        )
        total_nfts += len(nfts)
        if len(nfts) == 0:
            break

        processed_nfts: list[NftWithTags] = []
        for nft in nfts:
            tags: list[TagWithValue] = [
                (tag, value)
                for (tag, value) in tokenization_service.tokenize(nft).items()
            ]
            processed_nfts.append((nft, tags))
        transaction_service.insert_nfts(processed_nfts)
        offset_tokens += tx_limit
    print(f"Unique tokens processed:                        {total_nfts}")


def process_transfers(
    repo, indexer_service, transaction_service, start_block, block_count, tx_limit
):
    totalTransfers = len(repo.get_transfers())
    offset = 0
    while repo.has_transfers():
        transaction_service.populate_db()
        repo.clear()
        offset += tx_limit
        newtransfers = indexer_service.fetch_transfers(
            start_block, start_block + block_count, offset, tx_limit
        )
        repo.save(newtransfers)
        totalTransfers += len(newtransfers)

    print(f"Unique transfers processed:                     {totalTransfers}")


def main():
    start_raw = input("Start block (12337801) (blank for 12337801): ")
    start_block = 12337801 if start_raw == "" else int(start_raw)
    block_count = int(input("Block batch count: "))
    tx_limit = int(input("Transaction batch count: "))

    process_data(start_block, block_count, tx_limit)


def main_server():
    process_data(0, 1000, 1000)
