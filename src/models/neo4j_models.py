from dataclasses import dataclass
from typing import Optional


@dataclass
class NFT:
    address: str
    tokenId: int
    createdAtBlock: int
    name: Optional[str] = None
    uri: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[tuple[dict]] = None
    image: Optional[str] = None
    raw: Optional[str] = None
    externalUrl: Optional[str] = None
    animationUrl: Optional[str] = None


@dataclass
class Address:
    address: str
    createdAtBlock: int


@dataclass
class Transaction:
    id: str
    amount: int
    nft_address: str
    from_address: str
    to_address: str
