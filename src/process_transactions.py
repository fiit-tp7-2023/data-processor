from src.services.IndexerService import IndexerService
from src.services.TransactionService import TransactionService
from src.services.TokenizationService import TokenizationService
from src.database.neo4j import Neo4jDatabase
from src.repository.DataRepository import DataRepository
from src.tag_types import NftWithTags, TagWithValue


def main():
    indexer_service = IndexerService()
    tokenization_service = TokenizationService()
    transaction_service = TransactionService(Neo4jDatabase.get_instance().driver)
    repo = DataRepository.get_instance()
    
    repo.clear()
    start_block = int(input("Start block: "))
    block_count = int(input("Block batch count: "))
    tx_limit = int(input("Transaction batch count: "))
    while True:
        offset = 0
        print("Fetching data...")
        users = indexer_service.fetchUsers(start_block, start_block + block_count)
        transaction_service.insert_addresses(users)
        
        nfts = indexer_service.fetchTokens(start_block, start_block + block_count)
        processed_nfts: list[NftWithTags] = []
        for nft in nfts:
            tags: list[TagWithValue] = [(tag, value) for (tag, value) in tokenization_service.tokenize(nft).items()]
            processed_nfts.append((nft, tags))
            
        
        transaction_service.insert_nfts(processed_nfts)
        
        transfers = indexer_service.fetchTransfers(start_block, start_block + block_count, offset, tx_limit)
        repo.save(transfers)
        print("Data fetched successfully")
        while repo.has_transfers():
            print(f"[TX] {offset} - {offset + tx_limit}")
            transaction_service.populate_db(tx_limit)
            repo.clear()
            print("Fetching data...")
            offset += tx_limit
            transfers = indexer_service.fetchTransfers(start_block, start_block + block_count, offset, tx_limit)
            print("Data fetched successfully")
        start_block += block_count
        print(f"Next blocks: {start_block} - {start_block + block_count}")
