from src.services.IndexerService import IndexerService
from src.repository.DataRepository import DataRepository
from src.populate_neo import main as populate_neo
from src.fetch_data import main as fetch_data


def main():
    repo: DataRepository = DataRepository.get_instance()
    repo.clear()

    offset = 0
    limit = 3000
    from_block_id = 1
    total_processed = 0
    print("Fetching data...")
    fetch_data(limit, offset, from_block_id)
    print("Data fetched successfully")
    while repo.get_data_count() > 0:
        offset += limit
        total_processed += repo.get_data_count()
        populate_neo()
        print(f"Total processed: {total_processed} (offset: {offset}))")
        repo.clear()

        print("Fetching data...")
        fetch_data(limit, offset, from_block_id)
        print("Data fetched successfully")
