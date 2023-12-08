from neo4j import ManagedTransaction
from src.models.neo4j_models import Transaction, Address
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
        tx.run("CREATE CONSTRAINT address FOR (a:Address) REQUIRE (a.address) IS UNIQUE")
        tx.run("CREATE CONSTRAINT nft FOR (n:NFT) REQUIRE (n.address) IS UNIQUE")
        tx.run("CREATE CONSTRAINT tag FOR (t:Tag) REQUIRE (t.type) IS UNIQUE")
        
    # Insert NFTS 
    def _insert_nfts(tx: ManagedTransaction, data: list[NftWithTags]):
        formatted = [{
                "nft_address": nft.address,
                "nft_token_id": nft.tokenId,
                "nft_name": nft.name,
                "nft_image": nft.image,
                "nft_uri": nft.uri,
                "nft_raw": nft.raw,
                "nft_external_url": nft.externalUrl,
                "nft_created_at_block": nft.createdAtBlock,
                "nft_animation_url": nft.animationUrl,
                "nft_description": nft.description,
                "nft_attributes": str(nft.attributes),
            } for (nft, _) in data]

        query = """
        UNWIND $props AS data
        CREATE (n:NFT {address: data.nft_address})
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
        
        if any("nft_image" in entry for entry in formatted):
            set_statements.append("n.image = data.nft_image")
        
        if any("nft_raw" in entry for entry in formatted):
            set_statements.append("n.raw = data.nft_raw")
        
        if any("nft_external_url" in entry for entry in formatted):
            set_statements.append("n.externalUrl = data.nft_external_url")
        
        if any("nft_animation_url" in entry for entry in formatted):
            set_statements.append("n.animationUrl = data.nft_animation_url")
            
        if any("nft_created_at_block" in entry for entry in formatted):
            set_statements.append("n.createdAtBlock = data.nft_created_at_block")
            
        if any("nft_token_id" in entry for entry in formatted):
            set_statements.append("n.tokenId = data.nft_token_id")
            

        if len(set_statements) > 0:
            query += " SET "+ ", ".join(set_statements)

        tx.run(query, props=formatted)
        
        # Now insert tags with relation to NFT
        query = """
        UNWIND $props AS data
        MATCH (n:NFT {address: data.nft_address})
        MERGE (t:Tag {type: data.tag_type})
        MERGE (t)<-[:TAGGED { value: data.relation_weight }]-(n)
        """
        
        for (nft, tags) in data:
            formatted = [{
                "nft_address": nft.address,
                "tag_type": tag,
                "relation_weight": weight
            } for tag, weight in tags]
            tx.run(query, props=formatted)


    # INSERT ADDRESSES
    @staticmethod
    def _insert_addresses(tx: ManagedTransaction, addresses: list[Address]):
        query = """
        UNWIND $props AS data
        MERGE (a:Address {address: data.address, createdAtBlock: data.createdAtBlock})
        """
        tx.run(query, props=[{"address":a.address, "createdAtBlock":a.createdAtBlock} for a in addresses])


    # INSERT ADDRESSES
    @staticmethod
    def _insert_transactions(tx: ManagedTransaction, transactions: list[Transaction]):
        query = """
        UNWIND $props AS data
        MATCH (from:Address {address: data.from_address}),
        (to: Address {address: data.to_address}),
        (n:NFT {address: data.nft_address})
        MERGE (from)-[:SENT]->(t:Transaction {id: data.transaction_id, amount: toInteger(data.amount)})<-[:RECEIVED]-(to)
        MERGE (n)-[:HAS_NFT]->(t)
        """
        
        tx.run(query, props=[{"transaction_id":t.id, "to_address": t.to_address , "from_address":t.from_address, "nft_address": t.nft_address , "amount": t.amount } for t in transactions])
