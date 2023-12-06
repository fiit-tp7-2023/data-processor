from src import fetch_data
from src import populate_neo
from src.database.neo4j import Neo4jDatabase
from src.services.TransactionService import TransactionService
from src import process_transactions
import json
from typing import Dict, Tuple
from src.models.neo4j_models import NFT

class Program:
    def run():
        driver = Neo4jDatabase.get_instance().driver
        transaction_service = TransactionService(driver)
        transaction_service.init_db()
        print("Welcome to the NFT Graph Python DATA PROCESSING program")
        while True:
            print("_" * 50)
            print("Please select an option:")
            print("1. Process transactions")
            print("2. Reset neo4j database")
            print("3. Exit")
            print("4. Try tokenization")
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
            
            elif option == "4":
                print("Trying tokenization...")
                nft = NFT(
                    id="1",
                    name="Graphene Batteries",
                    description= "They are more of a slow release explosion than a battery. Comprised of highly volatile chemicals, it has a singular cycle life and outputs immense amounts of energy. Handle with fear lest we all feel the catastrophic consequences. ",
                    uri="uri",
                    attributes=[{"key": "Rarity", "value": "Uncommon", "trait_type": "Rarity"}, {"key": "Class", "value": "First Edition", "trait_type": "Class"}, {"key": "Artist", "value": "Oscar Mar", "trait_type": "Artist"}, {"key": "Parallel", "value": "Augencore", "trait_type": "Parallel"}] 
                )
                from src.services.TokenizationService import TokenizationService
                tokenization_service = TokenizationService()
                print(len(tokenization_service.tokenize(nft).items()))
                print("\nTokenization done successfully\n")
