from pymongo import MongoClient
from config.settings import MONGODB_URI, DATABASE_NAME
import certifi  # Añadimos esto para manejar certificados

class MongoDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDAO, cls).__new__(cls)
            try:
                # Modificamos la conexión con dos parámetros de seguridad
                cls._instance.client = MongoClient(
                    MONGODB_URI,
                    tlsCAFile=certifi.where(), # Usa certificados actualizados
                    tlsAllowInvalidCertificates=True # Ignora bloqueos de firewall/antivirus
                )
                cls._instance.db = cls._instance.client[DATABASE_NAME]
                
                # Test de conexión
                cls._instance.client.admin.command('ping')
                print("Conexión a MongoDB: OK")
            except Exception as e:
                print(f"Error crítico de conexión DB: {e}")
                cls._instance.db = None
        return cls._instance

    def insertar_sesion(self, sesion):
        if self.db is not None:
            return self.db.sessions.insert_one(sesion)

    def insertar_evento(self, evento):
        if self.db is not None:
            return self.db.volume_events.insert_one(evento)