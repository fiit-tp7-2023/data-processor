from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship
import os
from neomodel import config
from dotenv import load_dotenv


load_dotenv()
#TODO add config.URL for neomodels 
config.DATABASE_URL = ''

class Address(StructuredNode):
    address = StringProperty(required=True, index=True, unique=True)
    transactions_sent = Relationship('Transaction', 'SENT')
    transactions_received = Relationship('Transaction', 'RECEIVED')


class NFT(StructuredNode):
    nft_id = StringProperty(unique_index=True)
    transactions = Relationship('Transaction', 'NFT')


class Transaction(StructuredNode):
    transaction_id = StringProperty(unique_index=True)
    amount = StringProperty()
    from_address = RelationshipTo(Address, 'SENT')
    to_address = RelationshipTo(Address, 'RECEIVED')
    nft_id = RelationshipTo(NFT, 'NFT')


