from conexion_db import DBConnection
import psycopg2

class UsuarioDAO:

    @staticmethod
    def registrar_usuario(nombre, foto_bytes):
        """
        Inserta un nuevo usuario en la base de datos.
        foto_bytes debe ser tipo bytes (BLOB)
        """
        conn = DBConnection.get_connection()
        if conn is None:
            print("No hay conexión a la base de datos.")
            return False

        try:
            cursor = conn.cursor()
            sql = "INSERT INTO usuarios (nombre, foto) VALUES (%s, %s)"
            cursor.execute(sql, (nombre, psycopg2.Binary(foto_bytes)))
            conn.commit()
            cursor.close()
            print(f"Usuario '{nombre}' registrado correctamente.")
            return True
        except psycopg2.Error as e:
            print(f"Error al registrar usuario: {e}")
            return False

    @staticmethod
    def obtener_todos():
        """
        Devuelve una lista de todos los usuarios en la BD.
        Cada elemento: (id, nombre, foto_bytes)
        """
        conn = DBConnection.get_connection()
        if conn is None:
            print("No hay conexión a la base de datos.")
            return []

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre, foto FROM usuarios")
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except psycopg2.Error as e:
            print(f"Error al obtener usuarios: {e}")
            return []
