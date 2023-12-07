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
                toAddress: {
                    id_not_startsWith: "0x00"
                }, 
                fromAddress: {
                    id_not_startsWith: "0x00"
                },
                createdAtBlock_gt : $blockId
            }

        ) {
            id
            amount
            fromAddress {
                id
            }
            nft {
                id
                name
                attributes
                description
                uri
            }
            toAddress {
                id
            }
        }
    }
    """

    variables = {"blockId": from_block_id, "limit": limit, "offset": offset}
    parsed = service.runQuery(query, variables)
    transfers = parsed["data"]["nftTransferEntities"]
    for transfer in transfers:
        repo.save(transfer)
