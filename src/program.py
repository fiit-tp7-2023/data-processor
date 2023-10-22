
from src import fetch_data
from src import populate_neo
from src.database.neo4j import Neo4jDatabase


class Program:

    def run():
        while True:
            print("Welcome to the NFT Graph Python DATA PROCESSING program")
            print("_"*50)
            print("Please select an option:")
            print("1. Process data from indexer")
            print("2. Populate neo4j database with data from /src/logs/indexer_data/indexer.log")
            print("3. Reset neo4j database")
            print("4. Exit")
            print("_"*50)

            option = input("Option: ")

            if option == "1":
                print("Processing data from indexer...")
                fetch_data.main()
                print("\nData processed successfully\n")

            elif option == "2":
                print("Populating neo4j database...")
                populate_neo.main()
                print("\nNeo4j database populated successfully\n")

            elif option == "3":
                print("Resetting neo4j database...")
                Neo4jDatabase.get_instance().reset_database()
                print("\nNeo4j database reset successfully\n")

            elif option == "4":
                print("Exiting program...")
                break






        



