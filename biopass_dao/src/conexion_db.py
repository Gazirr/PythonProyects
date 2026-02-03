import psycopg2
from psycopg2 import OperationalError
from config import Config

class DBConnection:
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None or cls._connection.closed != 0:
            try:
                cls._connection = psycopg2.connect(
                    host=Config.DB_HOST,
                    database=Config.DB_NAME,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    port=Config.DB_PORT
                )
                print("Conexión a la base de datos establecida.")
            except OperationalError as e:
                print(f"No se pudo conectar a la base de datos: {e}")
                cls._connection = None
        return cls._connection
