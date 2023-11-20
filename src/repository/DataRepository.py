from typing import Self

class DataRepository:
    _instance = None
    data: list[dict] = []

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataRepository, cls).__new__(cls)
        return cls._instance

    def get_instance() -> Self:
        if DataRepository._instance is None:
            DataRepository._instance = DataRepository()
        return DataRepository._instance
    
    def get_data(self) -> list[dict]:
        return self.data

    def get_data_count(self) -> int:
        return len(self.data)

    def save(self, data: dict):
        self.data.append(data)

    def clear(self):
        self.data = []