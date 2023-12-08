from dataclasses import dataclass

@dataclass
class NFT():
    address: str
    tokenId: int
    createdAtBlock: int
    name: str | None = None
    uri: str | None = None
    description: str | None = None
    attributes: tuple[dict] | None = None
    image: str | None = None
    raw: str | None = None
    externalUrl: str | None = None
    animationUrl: str | None = None

@dataclass
class Address():
    address: str
    createdAtBlock: int

@dataclass
class Transaction():
    id: str
    amount: int
    nft_address: str
    from_address: str
    to_address: str
   

