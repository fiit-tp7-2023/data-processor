from neo4j import GraphDatabase, Driver, ManagedTransaction


class Neo4jDatabase:
    _instance = None

    def __new__(cls, uri, user, password):
        if cls._instance is None:
            cls._instance = super(Neo4jDatabase, cls).__new__(cls)
            cls._instance.init_database(uri, user, password)
        return cls._instance

    def get_instance():
        return Neo4jDatabase._instance

    def init_database(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def reset_database(self):
        nodes_deleted = 1
        while nodes_deleted != 0:
            records, summary, keys = self.driver.execute_query(
                """MATCH (n) WITH n LIMIT 300 DETACH DELETE n RETURN count(n) AS nodesDeleted"""
            )
            print(records)
            for record in records:
                nodes_deleted = record[
                    keys[0]
                ]  # Accessing the value using the first key

        self.driver.execute_query("DROP CONSTRAINT address IF EXISTS")
        self.driver.execute_query("DROP CONSTRAINT nft IF EXISTS")
        self.driver.execute_query("DROP CONSTRAINT tag IF EXISTS")

    @staticmethod
    def _run_query(tx: ManagedTransaction, query):
        result = tx.run(query)
        return result
