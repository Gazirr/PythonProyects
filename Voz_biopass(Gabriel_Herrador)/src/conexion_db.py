import psycopg # Cambiado de psycopg2
from config import Config

class ConexionDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConexionDB, cls).__new__(cls)
            cls._instance.connection = None
            try:
                # Debugging info
                conn_str_debug = f"dbname={Config.DB_NAME} user={Config.DB_USER} host={Config.DB_HOST} port={Config.DB_PORT}"
                print(f"Intentando conectar a DB: {conn_str_debug}")
                
                cls._instance.connection = psycopg.connect(
                    conninfo=f"dbname={Config.DB_NAME} user={Config.DB_USER} password={Config.DB_PASSWORD} host={Config.DB_HOST} port={Config.DB_PORT}"
                )
                print("Conexión a la base de datos establecida.")
            except Exception as e:
                print(f"Error CRÍTICO al conectar a la base de datos: {e}")
        return cls._instance

    def get_connection(self):
        return self.connection

    def close_connection(self):
        if self.connection:
            self.connection.close()
            ConexionDB._instance = None
            print("Conexión a la base de datos cerrada.")
