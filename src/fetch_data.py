from src.services.IndexerService import IndexerService
from src.repository.DataRepository import DataRepository



def main():
    repo: DataRepository = DataRepository.get_instance()
    repo.clear()
    
    service = IndexerService()
    query = {
        "operationName": "getTransactions",
        "variables": None,
        "query": """query getTransactions {
            nftTransferEntities(
                limit: 1000,
                where: {
                    toAddress_not_contains: "0x00",
                    fromAddress_not_contains: "0x00",
                    nft: {
                        name_isNull: false
                    }
                }
            )
            {
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
        }
   
    parsed = service.runQuery(query)
    transfers = parsed['data']['nftTransferEntities']
    for transfer in transfers:
        repo.save(transfer)