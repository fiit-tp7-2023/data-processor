from neomodel import StructuredNode, StringProperty, RelationshipTo, Relationship, cardinality


class Address(StructuredNode):
    _id = StringProperty(required=True, index=True, unique=True)
    transactions_sent = Relationship('Transaction', 'SENT')
    transactions_received = Relationship('Transaction', 'RECEIVED')


class NFT(StructuredNode):
    _id = StringProperty(unique_index=True, required=True)
    name = StringProperty(required=False)
    uri = StringProperty(required=False)
    description = StringProperty(required=False)
    attributes = StringProperty(required=False)
    tags = RelationshipTo('Tag', 'TAGGED', cardinality=cardinality.ZeroOrMore)


class Transaction(StructuredNode):
    _id = StringProperty(unique_index=True)
    amount = StringProperty()
    from_address = RelationshipTo(Address, 'SENT')
    to_address = RelationshipTo(Address, 'RECEIVED')
    nft = RelationshipTo(NFT, 'NFT', cardinality=cardinality.One)
    
class Tag(StructuredNode):
    _id = StringProperty(unique_index=True)
    type: StringProperty()


