from src.models.neo4j_models import Transaction
from src.repository.TransactionRepository import TransactionRepository
from neo4j import Driver

class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver

    def close(self):
        self.driver.close()
        
    def processMultipleTransactions(self, transactions: list[Transaction]):
        data = []
        for t in transactions:
            data.append(t.from_address)
            data.append(t.to_address)
            
        addresses = list(set(data))
        self.insert_addresses(addresses)
        self.insert_transactions(transactions)

    def processTransaction(self, transaction: Transaction):
        
        if not self.isAddressInGraph(transaction.from_address):
            self.insert_address(transaction.from_address)

        if not self.isAddressInGraph(transaction.to_address):
            self.insert_address(transaction.to_address)

        self.insert_transaction(transaction)
            
    def isAddressInGraph(self, address: str):
        with self.driver.session() as session:
            return session.read_transaction(TransactionRepository._is_address_in_graph, address)


    def insert_address(self, address: str):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_address, address)
            
    def insert_addresses(self, addresses: list[str]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_addresses, addresses)


    def insert_transaction(self, data: Transaction):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transaction_with_nft, data)
            session.write_transaction(TransactionRepository._create_transaction_relationships, data)

    def insert_transactions(self, transactions: list[Transaction]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transactions_with_nft, transactions)
            session.write_transaction(TransactionRepository._create_transaction_relationships_multiple, transactions)

    