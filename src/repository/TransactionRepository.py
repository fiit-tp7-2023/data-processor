from neo4j import ManagedTransaction
from src.models.neo4j_models import Transaction
from src.tag_types import NftWithTags, TransactionWithTags


class TransactionRepository:
    def _init_db(tx: ManagedTransaction):
        constraints = tx.run("SHOW CONSTRAINTS")
        # If constraints already exist, do not create them again
        if constraints.peek() is not None:
            return

        tx.run(
            "CREATE CONSTRAINT transaction FOR (t:Transaction) REQUIRE (t.id) IS UNIQUE"
        )
        tx.run("CREATE CONSTRAINT address FOR (a:Address) REQUIRE (a.id) IS UNIQUE")
        tx.run("CREATE CONSTRAINT nft FOR (n:NFT) REQUIRE (n.id) IS UNIQUE")
        tx.run("CREATE CONSTRAINT tag FOR (t:Tag) REQUIRE (t.type) IS UNIQUE")
        
    # Insert NFTS 
    def _insert_nfts(tx: ManagedTransaction, data: list[tuple[NftWithTags, str]]):
        formatted = [{
                "nft_id": nft.id,
                "nft_name": nft.name,
                "nft_uri": nft.uri,
                "nft_description": nft.description,
                "nft_attributes": str(nft.attributes),
                "transaction_id": transaction_id
            } for (nft, _), transaction_id in data]

        query = """
        UNWIND $props AS data
        MATCH (t:Transaction {id: data.transaction_id})
        MERGE (n:NFT {id: data.nft_id})
        MERGE (t)-[:HAS_NFT]->(n)
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
            query = query % "ON CREATE SET " + ", ".join(set_statements)

        tx.run(query, props=formatted)
        
        # Now insert tags with relation to NFT
        query = """
        UNWIND $props AS data
        MATCH (n:NFT {id: data.nft_id})
        MERGE (t:Tag {type: data.tag_type})
        MERGE (t)<-[:TAGGED { value: data.relation_weight }]-(n)
        """
        
        for (nft, tags), _ in data:
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
    @staticmethod
    def _insert_transactions(tx: ManagedTransaction, transactions: list[Transaction]):
        query = """
        UNWIND $props AS data
        MATCH (from:Address {id: data.from_address}),
        (to: Address {id: data.to_address})
        MERGE (from)-[:SENT]->(t:Transaction {id: data.transaction_id, amount: toInteger(data.amount)})<-[:RECEIVED]-(to)
        """
        
        tx.run(query, props=[{"transaction_id":t.id, "to_address":t.to_address, "from_address":t.from_address, "amount": t.amount } for t in transactions])
