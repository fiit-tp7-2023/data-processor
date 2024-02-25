from src.models.neo4j_models import NFT, Transaction, Token

type NftAttributes = dict[str, str]

type TagWithValue = tuple[str, int]

type NftWithTags = tuple[NFT, list[TagWithValue]]

type TransactionWithTags = tuple[Transaction, NftWithTags]

type TransactionWithToken = tuple[Transaction, Token]