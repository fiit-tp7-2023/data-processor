from src.models.neo4j_models import Transaction, NFT
from src.repository.TransactionRepository import TransactionRepository
from neo4j import Driver

class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver

    def close(self):
        self.driver.close()
        
    def processMultipleTransactions(self, transactions: list[Transaction]):
        addresses = []
        for t in transactions:
            addresses.append(t.from_address)
            addresses.append(t.to_address)
            
        addresses = list(set(addresses))

        nfts = []
        for t in transactions:
            nft = NFT(
                id=t.nft.get('id', ' '),
                name=t.nft.get('name', ' '),
                uri=t.nft.get('uri', ' '),
                description=t.nft.get('description', ' ')
            )
            nfts.append(nft)

        self.insert_nfts(nfts)
        self.insert_addresses(addresses)
        self.insert_transactions(transactions)
        self.insert_relations(transactions)
            
            
    def insert_addresses(self, addresses: list[str]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_addresses, addresses)

    def insert_nfts(self, nfts: list[NFT]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_nfts, nfts)

    def insert_transactions(self, transactions: list[Transaction]):
         with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transactions, transactions)

    def insert_relations(self, transactions: list[Transaction]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._relation_transaction_nft, transactions)
            session.write_transaction(TransactionRepository._relation_transaction_address, transactions)

    