from config.db_config import get_db_config
from src.database.postgres import PostgreSQLDatabase
from src.database.neo4j import Neo4jDatabase
from src.data_processing import DataProcessor
from src.logs.logger import DataProcessingLogger

# Load database configurations from db_config.json
db_config = get_db_config()

# Initialize and connect to PostgreSQL
pg_db = PostgreSQLDatabase(db_config['pg_config'])
pg_db.connect()

# Initialize and connect to Neo4j
neo4j_db = Neo4jDatabase(
    db_config['neo4j_uri'],
    db_config['neo4j_user'],
    db_config['neo4j_password']
)
neo4j_db.connect()

# Initialize data processor
data_processor = DataProcessor()

# Initialize logger
logger = DataProcessingLogger("config/logs/data_processing.log")

# Fetch data from PostgreSQL and process it
pg_db.execute_query("SELECT * FROM your_pg_table")
for row in pg_db.fetch_data():
    processed_data = data_processor.process_data(row)
    # Logging the processed data (example)
    logger.log(f"Processed data: {processed_data}")
    # Create nodes in Neo4j (example)
    neo4j_db.create_node("Data", {"value": processed_data})

# Close connections
pg_db.close()