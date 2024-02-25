from neo4j import ManagedTransaction
from src.models.neo4j_models import Transaction
from src.tag_types import NftWithTags, TransactionWithTags, TransactionWithToken


class TransactionRepository:

    # INSERT TOKENS
    @staticmethod
    def _insert_tokens(tx: ManagedTransaction, tokens: list[str]):
        query = """
        UNWIND $props AS data
        MERGE (t:Token {id: data.id, name: data.name})
        """
        tx.run(query, props=[{"id": t.id, "name": t.name} for t in tokens])

    # Insert NFTS 
    @staticmethod
    def _insert_nfts(tx: ManagedTransaction, data: list[NftWithTags]):
        formatted = [{
                "nft_id": nft.id,
                "nft_name": nft.name,
                "nft_uri": nft.uri,
                "nft_description": nft.description,
                "nft_attributes": nft.attributes
            } for nft, _ in data]

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
        
        # Now insert tags with relation to NFT
        query = """
        UNWIND $props AS data
        MATCH (n:NFT {id: data.nft_id})
        MERGE (t:Tag {type: data.tag_type})
        MERGE (n)-[:TAGGED { value: data.relation_weight }]->(t)
        """
        
        for nft, tags in data:
            formatted = [{
                "nft_id": nft.id,
                "tag_type": tag,
                "relation_weight": weight
            } for tag, weight in tags]
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
        
        tx.run(query, props=[{"transaction_id":t.id, "amount": t.amount } for t in transactions])


    # Create relation Address <- [:RECEIVED] - Transaction - [:SNET] -> Address
    @staticmethod
    def _relation_transaction_address(tx: ManagedTransaction, data: list[TransactionWithTags]):
        query = """
        UNWIND $props AS data
        MATCH (tx:Transaction {id: data.transaction_id}),
        (from:Address {id: data.from_address}),
        (to: Address {id: data.to_address})
        MERGE (from)-[:SENT]->(tx)<-[:RECEIVED]-(to)
        """
        formatted =[{"transaction_id":t.id, "to_address":t.to_address, "from_address":t.from_address } for t, _ in data]
        tx.run(query, props=formatted)

    # Create relation Transaction - [:HAS_TOKEN] -> Token
    @staticmethod
    def _relation_transaction_token(tx: ManagedTransaction, data: list[TransactionWithToken]):
        query = """
        UNWIND $props AS data
        MATCH (tx:Transaction {id: data.transaction_id}),
        (t:Token {id: data.token_id})
        MERGE (t)<-[:HAS_TOKEN]-(tx)
        """
        tx.run(query, props=[{"token_id": token.id,  "transaction_id":transaction.id} for transaction, token in data])


    # Create relation Transaction - [:HAS_NFT] -> NFT
    @staticmethod
    def _relation_transaction_nft(tx: ManagedTransaction, transactions: list[TransactionWithTags]):
        query = """
        UNWIND $props AS data
        MATCH (tx:Transaction {id: data.transaction_id}),
        (n:NFT {id: data.nft_id})
        MERGE (n)<-[:HAS_NFT]-(tx)
        """
        tx.run(query, props=[{"nft_id": nft.id,  "transaction_id":t.id} for t, (nft, _) in transactions])