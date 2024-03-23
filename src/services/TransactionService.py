from src.models.neo4j_models import Transaction, Address
from src.repository.TransactionRepository import TransactionRepository
from src.tag_types import NftWithTags, TransactionWithTags
from neo4j import Driver
from src.repository.DataRepository import DataRepository
from src.services.TokenizationService import TokenizationService
import time


class TransactionService:
    def __init__(self, db_driver: Driver):
        self.driver = db_driver
        self.data_repository = DataRepository.get_instance()
        self.tokenization_service = TokenizationService()

    def close(self):
        self.driver.close()

    def init_db(self):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._init_db)

    def populate_db(self):
        data = self.data_repository.get_transfers()
        transactions: list[Transaction] = []
        for item in data:
            transactions.append(
                Transaction(
                    id=item["id"],
                    amount=item["amount"],
                    from_address=item["fromAddress"]["id"],
                    to_address=item["toAddress"]["id"],
                    nft_address=item["nft"]["id"],
                )
            )

        self.insert_transactions(transactions)
        end_time = time.time()
        print(f"Finished populating in {end_time - start_time} seconds")

    def insert_addresses(self, addresses: list[Address]):
        with self.driver.session() as session:
            session.write_transaction(
                TransactionRepository._insert_addresses, addresses
            )

    def insert_nfts(self, nfts: list[(NftWithTags, str)]):
        with self.driver.session() as session:
            session.write_transaction(TransactionRepository._insert_nfts, nfts)

    def insert_transactions(self, transactions: list[Transaction]):
        with self.driver.session() as session:
            session.write_transaction(
                TransactionRepository._insert_transactions, transactions
            )

    def fetch_nfts(self, count: int):
        with self.driver.session() as session:
            return session.read_transaction(TransactionRepository._fetch_nfts, count)
