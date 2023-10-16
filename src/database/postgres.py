import psycopg2

class PostgreSQLDatabase:
    def __init__(self, pg_config):
        self.pg_config = pg_config
        self.pg_conn = None
        self.pg_cursor = None

    def connect(self):
        self.pg_conn = psycopg2.connect(**self.pg_config)
        self.pg_cursor = self.pg_conn.cursor()

    def execute_query(self, query, params=None):
        self.pg_cursor.execute(query, params)

    def fetch_data(self):
        return self.pg_cursor.fetchall()

    def close(self):
        self.pg_cursor.close()
        self.pg_conn.close()