from src.services.IndexerService import IndexerService
from src.repository.DataRepository import DataRepository


def main(limit: int, offset: int, from_block_id: int):
    repo: DataRepository = DataRepository.get_instance()
    repo.clear()

    service = IndexerService()
    query = """
        query getTransactions($blockId: Int!, $limit: Int!, $offset: Int!) {
        nftTransferEntities(
            orderBy: createdAtBlock_ASC
            limit: $limit,
            offset: $offset,
            where: {
                toAddress_not_contains: "0x00",
                fromAddress_not_contains: "0x00",
                createdAtBlock_gt : $blockId
            }

        ) {
            amount
            id
            fromAddress
            toAddress
            nft {
                id
                name
                description
                uri
                attributes
            }
        }
        }
    """

    variables = {"blockId": from_block_id, "limit": limit, "offset": offset}
    parsed = service.runQuery(query, variables)
    transfers = parsed["data"]["nftTransferEntities"]
    for transfer in transfers:
        repo.save(transfer)
