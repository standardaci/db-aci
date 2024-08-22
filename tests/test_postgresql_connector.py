import unittest
from unittest.mock import patch, MagicMock
from src.connectors.postgresql_connector import PostgreSQLConnector

class TestPostgreSQLConnector(unittest.TestCase):
    @patch('psycopg2.connect')
    def test_execute_query(self, mock_connect):
        mock_cur = MagicMock()
        mock_cur.fetchall.return_value = [{"id": 1, "name": "Test"}]
        mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cur

        connector = PostgreSQLConnector("mock_connection_string")
        result = connector.execute_query("SELECT * FROM test")

        self.assertEqual(result, [{"id": 1, "name": "Test"}])
        mock_cur.execute.assert_called_once_with("SELECT * FROM test")

    # Add more tests for get_schema and error handling
