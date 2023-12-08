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
        transfers = indexer_service.fetch_transfers(start_block, start_block + block_count, 0, tx_limit)
        repo.save(transfers)
        if len(transfers) == 0:
            start_block += block_count
            continue
        
        total_start = time.time()
        print(f"Blocks: {start_block} - {start_block + block_count}")
            
        print("Fetching users...")
        offset_users = 0
        while True:
            users = indexer_service.fetch_users(start_block, start_block + block_count, offset_users, tx_limit)
            if len(users) == 0:
                break
            transaction_service.insert_addresses(users)
            offset_users += tx_limit
        print("Users inserted successfully")
        print("Fetching tokens...")
        offset_tokens = 0
        while True:
            nfts = indexer_service.fetch_tokens(start_block, start_block + block_count, offset_tokens, tx_limit)
            if len(nfts) == 0:
                break
            
            processed_nfts: list[NftWithTags] = []
            print(f"Tokenizing batch of {len(nfts)} nfts...")
            for nft in nfts:
                tags: list[TagWithValue] = [(tag, value) for (tag, value) in tokenization_service.tokenize(nft).items()]
                processed_nfts.append((nft, tags))
            transaction_service.insert_nfts(processed_nfts)  
            offset_tokens += tx_limit
        print("Tokens inserted successfully")
        print("Processing transfers...")
        offset = 0
        while repo.has_transfers():
            transaction_service.populate_db()
            repo.clear()
            offset += tx_limit
            repo.save(indexer_service.fetch_transfers(start_block, start_block + block_count, offset, tx_limit))
        start_block += block_count
        total_end = time.time()
        print(f"Finished processing in {total_end - total_start} seconds")
