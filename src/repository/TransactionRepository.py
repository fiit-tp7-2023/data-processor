
class TransactionRepository:
    
    # UTIL FUNCTION, IS ADDRESS IN GRAPH ?
    @staticmethod  
    def _is_address_in_graph(tx, address):
        query = (
            "MATCH (a:Address) WHERE a.address = $address RETURN a"
        )
        result = tx.run(query, address=address)
        return result.single() is not None


    # INSERT NFT INTO GRAPH DATABASE
    @staticmethod
    def _insert_transaction_with_nft(tx, transaction, nft):
        query = (
            "MERGE (n:NFT {nft_id: $nft_id}) - [:NFT] -> (t:Transaction {transaction_id: $transaction_id})"
        )
        tx.run(query, nft_id=nft, transaction_id=transaction)


    # INSERT ADDRESS INTO GRAPH DATABASE
    @staticmethod
    def _insert_address(tx, address):
        query = (
            "MERGE (a:Address {address: $address})"
        )
        tx.run(query, address=address)
        
    # CREATE SENT RELATIONSHIP BETWEEN TRANSACTION AND ADDRESSES
    @staticmethod
    def _create_transaction_relationships(tx, transaction_id, from_address, to_address):
        print(f"MATCH (tx:Transaction), (from:Address), (to: Address) WHERE tx.transaction_id = ${transaction_id} AND from.address = ${from_address} AND to.address = ${to_address} CREATE (from)-[:SENT]->(tx)<-[:RECEIVED]-(to)")
        query = "MATCH (tx:Transaction), (from:Address), (to: Address) WHERE tx.transaction_id = $transaction_id AND from.address = $from_address AND to.address = $to_address CREATE (from)-[:SENT]->(tx)<-[:RECEIVED]-(to)"
        tx.run(query,  transaction_id=transaction_id, from_address=from_address, to_address= to_address)
