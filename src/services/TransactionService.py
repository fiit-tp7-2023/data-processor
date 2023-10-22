from neo4j import GraphDatabase
import json
from src.models.neo4j_models import Transaction

class TransactionService:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def processTransaction(self, transaction: Transaction):
        if not self.isAddressInGraph(transaction.from_address):
            self.insert_address(transaction.from_address)

        if not self.isAddressInGraph(transaction.to_address):
            self.insert_address(transaction.to_address)

        self.insert_transaction(transaction.from_address, transaction.to_address, transaction.transaction_id, transaction.nft)
            
    def isAddressInGraph(self, address):
        with self.driver.session() as session:
            return session.read_transaction(self._is_address_in_graph, address)


    def insert_address(self, address):
        with self.driver.session() as session:
            session.write_transaction(self._insert_address, address)


    def insert_transaction(self, from_address, to_address, transaction, nft):
        with self.driver.session() as session:
            session.write_transaction(self._create_sent_relationship, from_address, to_address)
            session.write_transaction(self._create_received_relationship, from_address, to_address)
            session.write_transaction(self._insert_nft, transaction, nft)
            session.write_transaction(self._create_nft_relationship, transaction, nft)


    # UTIL FUNCTION, IS ADDRESS IN GRAPH ?
    @staticmethod  
    def _is_address_in_graph(tx, address):
        query = (
            "MATCH (a:Address) WHERE a.address = $address RETURN a"
        )
        result = tx.run(query, address=address)
        return result.single() is not None


    # INSERT NFT INTO GRAPH DATABASE
    @staticmethod
    def _insert_nft(tx, transaction, nft):
        query = (
            "MERGE (n:NFT {nft_id: $nft_id}) "
            "MERGE (t:Transaction {transaction_id: $transaction_id}) "
            "MERGE (t)-[:NFT]->(n)"
        )
        tx.run(query, nft_id=nft, transaction_id=transaction)


    # INSERT ADDRESS INTO GRAPH DATABASE
    @staticmethod
    def _insert_address(tx, address):
        query = (
            "MERGE (a:Address {address: $address})"
        )
        tx.run(query, address=address)


    # CREATE RELATIONSHIP BETWEEN ADDRESSES SENT
    @staticmethod
    def _create_sent_relationship(tx, from_address, to_address):
        query = "MATCH (from:Address), (to:Address) WHERE from.address = $from_address AND to.address = $to CREATE (from)-[:SENT]->(to)"
        tx.run(query, from_address=from_address, to=to_address)


    # CREATE RELATIONSHIP BETWEEN ADDRESSES RECEIVED
    @staticmethod
    def _create_received_relationship(tx, from_address, to_address):
        query = "MATCH (from:Address), (to:Address) WHERE from.address = $from_address AND to.address = $to CREATE (from)<-[:RECEIVED]-(to)"
        tx.run(query, from_address=from_address, to=to_address)


    # CREATE RELATIONSHIP BETWEEN TRANSACTION AND NFT
    @staticmethod
    def _create_nft_relationship(tx, transaction, nft):
        query = "MATCH (t:Transaction), (n:NFT) WHERE t.id = $transaction_id AND n.id = $nft_id CREATE (t)-[:NFT]->(n)"
        tx.run(query, transaction_id=transaction, nft_id=nft)