from dataclasses import dataclass

@dataclass
class NFT():
    id: str
    name: str | None = None
    uri: str | None = None
    description: str | None = None
    attributes: tuple[dict] | None = None

@dataclass
class Transaction():
    id: str
    amount: int
    from_address: str
    to_address: str
   

