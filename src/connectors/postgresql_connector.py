import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
from src.core.database_connector import DatabaseConnector

class PostgreSQLConnector(DatabaseConnector):
    def __init__(self, connection_string: str):
        self.conn = psycopg2.connect(connection_string)

    def execute_query(self, query: str) -> List[Dict[Any, Any]]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            return cur.fetchall()

    def get_schema(self) -> Dict[str, Any]:
        schema = {}
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT table_name, column_name, data_type
                FROM information_schema.columns
                WHERE table_schema = 'public'
            """)
            for table, column, data_type in cur.fetchall():
                if table not in schema:
                    schema[table] = []
                schema[table].append({"name": column, "type": data_type})
        return schema
