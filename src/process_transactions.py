from src.services.IndexerService import IndexerService
from src.services.TransactionService import TransactionService
from src.services.TokenizationService import TokenizationService
from src.database.neo4j import Neo4jDatabase
from src.repository.DataRepository import DataRepository
from src.tag_types import NftWithTags, TagWithValue
import time


def main():
    indexer_service = IndexerService()
    tokenization_service = TokenizationService()
    transaction_service = TransactionService(Neo4jDatabase.get_instance().driver)
    repo = DataRepository.get_instance()
    
    repo.clear()
    start_raw = input("Start block (12337801): ")
    if start_raw == "":
        start_block = 12337801
    else:
        start_block = int(start_raw)
    block_count = int(input("Block batch count: "))
    tx_limit = int(input("Transaction batch count: "))
    while True:
        offset = 0
        transfers = indexer_service.fetch_transfers(start_block, start_block + block_count, offset, tx_limit)
        if len(transfers) == 0:
            start_block += block_count
            continue
        
        
        print(f"Blocks: {start_block} - {start_block + block_count}")
            
        print("Fetching users...")
        users = indexer_service.fetch_users(start_block, start_block + block_count)
        print("Users fetched successfully")
        transaction_service.insert_addresses(users)
        print("Users inserted successfully")
        print("Fetching tokens...")
        nfts = indexer_service.fetch_tokens(start_block, start_block + block_count)
        processed_nfts: list[NftWithTags] = []
        print(f"Tokenizing {len(nfts)} nfts...")
        start = time.time()
        for nft in nfts:
            tags: list[TagWithValue] = [(tag, value) for (tag, value) in tokenization_service.tokenize(nft).items()]
            processed_nfts.append((nft, tags))
        end = time.time()
        print(f"Tokenization done in {end - start} seconds")
        transaction_service.insert_nfts(processed_nfts)
        print("Tokens inserted successfully")
        batch_count = 0
        repo.save(transfers)
        while repo.has_transfers():
            batch_count += 1
            print(f"Processing transfers in batch {batch_count}...")
            transaction_service.populate_db()
            repo.clear()
            offset += tx_limit
            repo.save(indexer_service.fetch_transfers(start_block, start_block + block_count, offset, tx_limit))
        start_block += block_count
