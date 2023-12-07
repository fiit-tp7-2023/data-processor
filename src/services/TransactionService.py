from src.models.neo4j_models import Transaction, NFT, Address
from src.repository.TransactionRepository import TransactionRepository
from src.tag_types import  NftWithTags, TransactionWithTags
from neo4j import Driver

class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver

    def close(self):
        self.driver.close()
        
    def init_db(self):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._init_db)
        
    def processMultipleTransactions(self, transactions: list[TransactionWithTags]):
        addresses: list[Address] = []
        for transaction, _ in transactions:
            addresses.append(transaction.from_address)
            addresses.append(transaction.to_address)
        used = set()
        addresses = [x for x in addresses if x.address not in used and (used.add(x.address) or True)]

        nfts: list[NftWithTags] = []
        pure_transactions: list[Transaction] = []
        for transaction, (nft, tags) in transactions:
            pure_transactions.append(transaction)
            nfts.append(((nft, tags), transaction.id))

        self.insert_addresses(addresses)
        self.insert_transactions(pure_transactions)
        self.insert_nfts(nfts)
            
            
    def insert_addresses(self, addresses: list[str]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_addresses, addresses)

    def insert_nfts(self, nfts: list[(NftWithTags, str)]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_nfts, nfts)

    def insert_transactions(self, transactions: list[Transaction]):
         with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transactions, transactions)

    