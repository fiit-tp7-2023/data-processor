import os
import requests
from src.models.neo4j_models import Address, NFT


class IndexerService:
    def __init__(self):
        self.indexer_uri = os.getenv("INDEXER_URI")

    def run_query(self, query, variables=None):
        raw = requests.post(
            self.indexer_uri + "/graphql",
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        return raw.json()
    
    
    def fetch_users(self, block_start: int, block_end: int) -> list[Address]:
        query = """
            query getUsers($blockStart: Int!, $blockEnd: Int!) {
            accountEntities(
                where: {createdAtBlock_gte: $blockStart, createdAtBlock_lt: $blockEnd, id_not_startsWith: "0x00"}, 
                orderBy: createdAtBlock_ASC
            ){
                id
                createdAtBlock
            }
        }
        """

        parsed = self.run_query(query, {"blockStart": block_start, "blockEnd": block_end})
        users = parsed["data"]["accountEntities"]
        return [Address(user["id"], user["createdAtBlock"]) for user in users]
    
    def fetch_tokens(self, block_start: int, block_end: int) -> list[NFT]:
        query = """
            query getTokens($blockStart: Int!, $blockEnd: Int!) {
                nftEntities(
                    where: {createdAtBlock_gte: $blockStart, createdAtBlock_lt: $blockEnd}, 
                    orderBy: createdAtBlock_ASC
                ) {
                    id
                    createdAtBlock
                    animationUrl
                    attributes
                    description
                    externalUrl
                    image
                    name
                    raw
                    tokenId
                    uri
                }
            }
        """
        
        parsed = self.run_query(query, {"blockStart": block_start, "blockEnd": block_end})
        raw_nfts = parsed["data"]["nftEntities"]
        nfts = []
        for nft in raw_nfts:
            nfts.append(NFT(
                address=nft["id"],
                tokenId=nft["tokenId"],
                createdAtBlock=nft["createdAtBlock"],
                name=nft["name"],
                uri=nft["uri"],
                description=nft["description"],
                attributes=nft["attributes"],
                image=nft["image"],
                raw=nft["raw"],
                externalUrl=nft["externalUrl"],
                animationUrl=nft["animationUrl"],
            ))
        return nfts
    
    def fetch_transfers(self, block_start:int, block_end: int, offset: int, limit: int) -> list[dict]:
        query = """
            query getTransactions($blockStart: Int!, $blockEnd: Int!, $limit: Int!, $offset: Int!) {
            nftTransferEntities(
                orderBy: createdAtBlock_ASC
                limit: $limit,
                offset: $offset,
                where: {
                    toAddress: {
                        id_not_startsWith: "0x00"
                    }, 
                    fromAddress: {
                        id_not_startsWith: "0x00"
                    },
                    createdAtBlock_gt : $blockStart,
                    createdAtBlock_lt : $blockEnd
                }

            ) {
                id
                amount
                fromAddress {
                    id
                }
                nft {
                    id
                }
                toAddress {
                    id
                }
            }
        }
        """
        variables = {"blockStart": block_start, "blockEnd": block_end, "limit": limit, "offset": offset}
        parsed = self.run_query(query, variables)
        transfers = parsed["data"]["nftTransferEntities"]
        return transfers
