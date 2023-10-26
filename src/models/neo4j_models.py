from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship
import os
from neomodel import config


class Address(StructuredNode):
    id = StringProperty(required=True, index=True, unique=True)
    transactions_sent = Relationship('Transaction', 'SENT')
    transactions_received = Relationship('Transaction', 'RECEIVED')


class NFT(StructuredNode):
    id = StringProperty(unique_index=True)
    name = StringProperty()
    uri = StringProperty()
    description = StringProperty()
    transactions = Relationship('Transaction', 'NFT')


class Transaction(StructuredNode):
    id = StringProperty(unique_index=True)
    amount = StringProperty()
    from_address = RelationshipTo(Address, 'SENT')
    to_address = RelationshipTo(Address, 'RECEIVED')
    nft_id = RelationshipTo(NFT, 'NFT')


