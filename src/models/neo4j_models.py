from dataclasses import dataclass

@dataclass
class NFT():
    id: str
    name: str | None = None
    uri: str | None = None
    description: str | None = None
    attributes: str | None = None

@dataclass
class Transaction():
    id: str
    amount: int
    from_address: str
    to_address: str

@dataclass
class Token():
    id: str
    name: str | None = None
   

