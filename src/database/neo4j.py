from neo4j import GraphDatabase

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
        with self.driver.session() as session:
            # Delete all nodes, relationships, and property keys
            query = "MATCH (n) DETACH DELETE n"
            session.write_transaction(self._run_query, query)

    @staticmethod
    def _run_query(tx, query):
        result = tx.run(query)
        return result
