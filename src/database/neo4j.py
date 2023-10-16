from neo4j import GraphDatabase

class Neo4jDatabase:
    def __init__(self, uri, user, password):
        self.uri = uri
        self.user = user
        self.password = password
        self.graph = None

    def connect(self):
        self.graph = GraphDatabase(self.uri, auth=(self.user, self.password))

    def create_node(self, label, properties):
        node = self.graph.nodes.create(label, **properties)
        return node