from neo4j import ManagedTransaction
from src.models.neo4j_models import Transaction
class TransactionRepository:
    
    # UTIL FUNCTION, IS ADDRESS IN GRAPH ?
    @staticmethod  
    def _is_address_in_graph(tx: ManagedTransaction, address: str):
        query = (
            "MATCH (a:Address) WHERE a.address = $address RETURN a"
        )
        result = tx.run(query, address=address)
        return result.single() is not None


    # INSERT NFT INTO GRAPH DATABASE
    @staticmethod
    def _insert_transaction_with_nft(tx: ManagedTransaction, data: Transaction):
        query = (
            "MERGE (n:NFT {nft_id: $nft_id}) - [:NFT] -> (t:Transaction {transaction_id: $transaction_id})"
        )
        tx.run(query, nft_id=data.nft_id, transaction_id=data.transaction_id)
        
    # INSERT MULTIPLE NFT INTO GRAPH DATABASE
    @staticmethod
    def _insert_transactions_with_nft(tx: ManagedTransaction, data: list[Transaction]):
        query = """
        UNWIND $props AS data
        MERGE (n:NFT {nft_id: data.nft_id}) - [:NFT] -> (t:Transaction {transaction_id: data.transaction_id})
        """
        tx.run(query, props=[{"nft_id": t.nft_id, "transaction_id":t.transaction_id } for t in data])


    # INSERT ADDRESS INTO GRAPH DATABASE
    @staticmethod
    def _insert_address(tx: ManagedTransaction, address: str):
        query = (
            "MERGE (a:Address {address: $address})"
        )
        tx.run(query, address=address)
        
        
    # INSERT ADDRESSES INTO GRAPH DATABASE
    @staticmethod
    def _insert_addresses(tx: ManagedTransaction, addresses: list[str]):
        raw_query = []
        for address in addresses:
            raw_query.append(f"(:Address {{address: '{address}'}})")
        query = f'CREATE {",".join(raw_query)}' 
        tx.run(query)
        
    # CREATE SENT RELATIONSHIP BETWEEN TRANSACTION AND ADDRESSES
    @staticmethod
    def _create_transaction_relationships(tx: ManagedTransaction, data: Transaction):
        query = "MATCH (tx:Transaction), (from:Address), (to: Address) WHERE tx.transaction_id = $transaction_id AND from.address = $from_address AND to.address = $to_address CREATE (from)-[:SENT]->(tx)<-[:RECEIVED]-(to)"
        tx.run(query,  transaction_id=data.transaction_id, from_address=data.from_address, to_address=data.to_address)
        
    
        
    # CREATE MULTIPLE SENT RELATIONSHIP BETWEEN TRANSACTION AND ADDRESSES
    @staticmethod
    def _create_transaction_relationships_multiple(tx: ManagedTransaction, data: list[Transaction]):
        query = """
        UNWIND $props AS data
        MATCH (tx:Transaction), (from:Address), (to: Address) 
        WHERE tx.transaction_id = data.transaction_id AND from.address = data.from_address AND to.address = data.to_address 
        CREATE (from)-[:SENT]->(tx)<-[:RECEIVED]-(to)
        """
        formatted =[{"nft_id": t.nft_id, "transaction_id":t.transaction_id, "to_address":t.to_address, "from_address":t.from_address } for t in data]
        tx.run(query, props=formatted)
