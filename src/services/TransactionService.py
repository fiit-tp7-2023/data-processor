from src.models.neo4j_models import Transaction
from src.repository.TransactionRepository import TransactionRepository
from neo4j import Driver

class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver

    def close(self):
        self.driver.close()

    def processTransaction(self, transaction: Transaction):
        if not self.isAddressInGraph(transaction.from_address):
            self.insert_address(transaction.from_address)

        if not self.isAddressInGraph(transaction.to_address):
            self.insert_address(transaction.to_address)

        self.insert_transaction(transaction.from_address, transaction.to_address, transaction.transaction_id, transaction.nft)
            
    def isAddressInGraph(self, address: str):
        with self.driver.session() as session:
            return session.read_transaction(TransactionRepository._is_address_in_graph, address)


    def insert_address(self, address: str):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_address, address)


    def insert_transaction(self, from_address: str, to_address: str, transaction_id: str, nft_id: str):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transaction_with_nft, transaction_id, nft_id)
            session.write_transaction(TransactionRepository._create_transaction_relationships, transaction_id, from_address, to_address)


    