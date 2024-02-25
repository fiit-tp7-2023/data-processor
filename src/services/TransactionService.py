from src.models.neo4j_models import Transaction, NFT, Token
from src.repository.TransactionRepository import TransactionRepository
from src.tag_types import  NftWithTags, TransactionWithTags
from neo4j import Driver

class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver

    def close(self):
        self.driver.close()
        
    def processMultipleTransactions(self, transactions: list[TransactionWithTags]):
        addresses: list[str] = []
        for transaction, _ in transactions:
            addresses.append(transaction.from_address)
            addresses.append(transaction.to_address)
            
        addresses = list(set(addresses))

        nfts: list[NftWithTags] = []
        pure_transactions: list[Transaction] = []
        for transaction, (nft, tags) in transactions:
            pure_transactions.append(transaction)
            nfts.append((nft, tags))

        self.insert_nfts(nfts)
        self.insert_addresses(addresses)
        self.insert_transactions(pure_transactions)
        self.insert_relations(transactions)
            
            
    def insert_addresses(self, addresses: list[str]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_addresses, addresses)
    
    def insert_tokens(self, tokens: list[Token]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_tokens, tokens)
        

    def insert_nfts(self, nfts: list[NftWithTags]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_nfts, nfts)

    def insert_transactions(self, transactions: list[Transaction]):
         with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_transactions, transactions)

    def insert_relations(self, transactions: list[TransactionWithTags]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._relation_transaction_nft, transactions)
            session.write_transaction(TransactionRepository._relation_transaction_address, transactions)

    