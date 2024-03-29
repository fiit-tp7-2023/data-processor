from src import program
import os
from dotenv import load_dotenv
from src.database.neo4j import Neo4jDatabase


if __name__ == "__main__":
    load_dotenv()
    neo4j_uri = os.getenv("NEO4J_URI")
    neo4j_user = os.getenv("NEO4J_USER")
    neo4j_password = os.getenv("NEO4J_PASSWORD")

    neo4j = Neo4jDatabase(neo4j_uri, neo4j_user, neo4j_password)

    # postgres = PostgresConnection(
    #     user=os.getenv("POSTGRES_USER"),
    #     password=os.getenv("POSTGRES_PASSWORD"),
    #     host=os.getenv("POSTGRES_HOST"),
    #     port=os.getenv("POSTGRES_PORT"),
    #     database=os.getenv("POSTGRES_DB"),
    # )
    program.Program.run()
