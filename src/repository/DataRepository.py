from typing import Self
from src.models.neo4j_models import Address

class DataRepository:
    _instance = None
    transfers: list[dict] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataRepository, cls).__new__(cls)
        return cls._instance

    def get_instance() -> Self:
        if DataRepository._instance is None:
            DataRepository._instance = DataRepository()
        return DataRepository._instance
    
    def get_transfers(self) -> list[dict]:
        return self.transfers

    def has_transfers(self) -> int:
        return len(self.transfers) > 0

    def save(self, transfers: dict):
        self.transfers.extend(transfers)

    def clear(self):
        self.transfers = []