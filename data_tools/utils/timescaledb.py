import psycopg2
from typing import List
import psycopg2.extras as ext
import config as cfg


class Timescaledb(object):
    """
    TimescaleDb connection
    """

    def __init__(self, db_name: str) -> None:
        """
        Initialize Timescaledb class
        Args:
            config: Get timescaledb config by file path or bunch object
        """
        self._connection = None
        self.database_name = db_name

    def __enter__(self):
        """
        Open timescaledb connection
        """
        try:
            self._connection = psycopg2.connect(host=cfg.TIMESCALEDB_GENERAL_HOST,
                                                database=self.database_name,
                                                port=cfg.TIMESCALEDB_GENERAL_PORT,
                                                user=cfg.TIMESCALEDB_GENERAL_USERNAME,
                                                password=cfg.TIMESCALEDB_GENERAL_PASSWORD)
            return self
        except Exception as e:
            print(f'Can not connect to timescaledb, {e}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        close Timescaledb connection
        """
        try:
            self._connection.close()
        except Exception as e:
            print(f'Timescaledb close connection is failed, {e}')

    def execute(self, query: str) -> bool:
        try:
            cursor = self._connection.cursor()
            cursor.execute(query)
            cursor.close()
            self._connection.commit()
            return True
        except Exception as e:
            print(f'Timescaledb execute query is failed, {e}')
            return False

    def read(self, query):
        try:
            cursor = self._connection.cursor(cursor_factory=ext.RealDictCursor)
            cursor.execute(query)
            coin = cursor.fetchall()
            cursor.close()
            self._connection.commit()
            return coin
        except Exception as e:
            print(f'Timescaledb execute query is failed, {e}')
            return False

    def insert(self, table: str, record: dict or List[dict]) -> int:
        """
        Insert record in table
        """
        try:
            fields = ','.join(record.keys())
            values = ','.join(record.values())
            query = f'INSERT INTO {table} ({fields}) VALUES({values})'
            cursor = self._connection.cursor()
            cursor.execute(query)
            cursor.close()
            self._connection.commit()
        except Exception as e:
            print(f'Insert in {table} is failed, {e}')
            return False
