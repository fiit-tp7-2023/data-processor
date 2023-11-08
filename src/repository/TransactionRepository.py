from neo4j import ManagedTransaction
from src.models.neo4j_models import Transaction, NFT
class TransactionRepository:


    # Insert NFTS 
    def _insert_nfts(tx: ManagedTransaction, data: list[NFT]):
        formatted = [{
                "nft_id": nft._id,
                "nft_name": nft.name,
                "nft_uri": nft.uri,
                "nft_description": nft.description,
                "nft_attributes": nft.attributes
            } for nft in data]

        query = """
        UNWIND $props AS data
        MERGE (n:NFT {id: data.nft_id})
        %s
        """
        set_statements = []

        if any("nft_name" in entry for entry in formatted):
            set_statements.append("n.name = data.nft_name")

        if any("nft_uri" in entry for entry in formatted):
            set_statements.append("n.uri = data.nft_uri")

        if any("nft_description" in entry for entry in formatted):
            set_statements.append("n.description = data.nft_description")

        if any("nft_attributes" in entry for entry in formatted):
            set_statements.append("n.attributes = data.nft_attributes")

        if len(set_statements) > 0:
            query = query % "SET " + ", ".join(set_statements)

        tx.run(query, props=formatted)


    # INSERT ADDRESSES
    @staticmethod
    def _insert_addresses(tx: ManagedTransaction, addresses: list[str]):
        query = """
        UNWIND $addresses AS address
        MERGE (a:Address {id: address})
        """
        tx.run(query, addresses=addresses)


    # INSERT ADDRESSES
    def _insert_transactions(tx: ManagedTransaction, transactions: list[Transaction]):
        query = """
        UNWIND $props AS data
        MERGE (t:Transaction {id: data.transaction_id, amount: toInteger(data.amount)})
        """
        tx.run(query, props=[{"transaction_id":t.transaction_id, "amount": t.amount } for t in transactions])


    # Create relation Address <- [:RECEIVED] - Transaction - [:SNET] -> Address
    @staticmethod
    def _relation_transaction_address(tx: ManagedTransaction, data: list[Transaction]):
        query = """
        UNWIND $props AS data
        MATCH (tx:Transaction {id: data.transaction_id}),
        (from:Address {id: data.from_address}),
        (to: Address {id: data.to_address})
        MERGE (from)-[:SENT]->(tx)<-[:RECEIVED]-(to)
        """
        formatted =[{"transaction_id":t.transaction_id, "to_address":t.to_address, "from_address":t.from_address } for t in data]
        tx.run(query, props=formatted)


    # Create relation Transaction - [:HAS_NFT] -> NFT
    @staticmethod
    def _relation_transaction_nft(tx: ManagedTransaction, transactions: list[Transaction]):
        query = """
        UNWIND $props AS data
        MATCH (tx:Transaction {id: data.transaction_id}),
        (n:NFT {id: data.nft_id})
        MERGE (n)<-[:HAS_NFT]-(tx)
        """
        tx.run(query, props=[{"nft_id": t.nft['id'], "nft_name": t.nft['name'], "nft_uri": t.nft['uri'], "nft_description": t.nft['description'], "transaction_id":t.transaction_id, "amount": t.amount } for t in transactions])