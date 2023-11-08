from src.models.neo4j_models import Transaction, NFT
from src.repository.TransactionRepository import TransactionRepository
from neo4j import Driver

class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver

    def close(self):
        self.driver.close()
        
    def processMultipleTransactions(self, transactions: list):
        addresses = []
        for transaction, tags in transactions:
            addresses.append(transaction.from_address)
            addresses.append(transaction.to_address)
            
        addresses = list(set(addresses))

        nfts = []
        pure_transactions = []
        for transaction, tags in transactions:
            nft = NFT(
                _id=transaction.nft.get('id', None),
                name=transaction.nft.get('name', None),
                uri=transaction.nft.get('uri', None),
                description=transaction.nft.get('description', None),
                attributes=str(transaction.nft.get('attributes', None))
            )
            pure_transactions.append(transaction)
            nfts.append((nft, tags))

        self.insert_nfts(nfts)
        self.insert_addresses(addresses)
        self.insert_transactions(pure_transactions)
        self.insert_relations(pure_transactions)
            
            
    def insert_addresses(self, addresses: list[str]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_addresses, addresses)

    def insert_nfts(self, nfts: list):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_nfts, nfts)

    def insert_transactions(self, transactions: list[Transaction]):
         with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transactions, transactions)

    def insert_relations(self, transactions: list[Transaction]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._relation_transaction_nft, transactions)
            session.write_transaction(TransactionRepository._relation_transaction_address, transactions)

    