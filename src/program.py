from src import fetch_data
from src import populate_neo
from src.database.neo4j import Neo4jDatabase
from src.services.TransactionService import TransactionService
from src import process_transactions


class Program:
    def run():
        driver = Neo4jDatabase.get_instance().driver
        transaction_service = TransactionService(driver)
        transaction_service.init_db()
        while True:
            print("Welcome to the NFT Graph Python DATA PROCESSING program")
            print("_" * 50)
            print("Please select an option:")
            print("1. Process transactions")
            print("2. Reset neo4j database")
            print("3. Exit")
            print("_" * 50)

            option = input("Option: ")

            if option == "1":
                print("Process Transactions")
                process_transactions.main()
                print("\nTransactions processed sucesfully\n")

            elif option == "2":
                print("Resetting neo4j database...")
                Neo4jDatabase.get_instance().reset_database()
                print("\nNeo4j database reset successfully\n")

            elif option == "3":
                print("Exiting program...")
                break
