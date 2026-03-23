import json
from datetime import datetime, timedelta
from conexion_db import ConexionDB
import psycopg # Cambiado a psycopg (v3)

class AuthDAO:
    def __init__(self):
        self.db = ConexionDB()
        self.conn = self.db.get_connection()

    def register_user(self, username, passphrase_text, result_json):
        """Registra un nuevo usuario y su primer log."""
        if not self.conn: return False
        try:
            with self.conn.cursor() as cur:
                # Insertar usuario
                cur.execute(
                    "INSERT INTO usuarios_voz (username, passphrase_text) VALUES (%s, %s) RETURNING id",
                    (username, passphrase_text)
                )
                user_id = cur.fetchone()[0]
                
                # Insertar log inicial
                cur.execute(
                    "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                    (user_id, json.dumps(result_json))
                )
                self.conn.commit()
                return True
        except Exception as e:
            print(f"Error en registro: {e}")
            self.conn.rollback()
            return False

    def get_user_by_username(self, username):
        """Busca un usuario por su nombre."""
        if not self.conn: return None
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT * FROM usuarios_voz WHERE username = %s", (username,))
                return cur.fetchone()
        except Exception as e:
            print(f"Error al buscar usuario: {e}")
            return None

    def login_attempt(self, user_id, status, extra_info=None):
        """Registra un intento de login en la tabla de logs (JSONB)."""
        if not self.conn: return
        try:
            resultado = {"status": status}
            if extra_info:
                resultado.update(extra_info)
            
            with self.conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                    (user_id, json.dumps(resultado))
                )
                
                # Actualizar intentos fallidos o resetear
                if status == "FAIL":
                    cur.execute("UPDATE usuarios_voz SET intentos_fallidos = intentos_fallidos + 1 WHERE id = %s", (user_id,))
                    # Verificar si debe bloquearse (ej. 3 intentos)
                    cur.execute("SELECT intentos_fallidos FROM usuarios_voz WHERE id = %s", (user_id,))
                    if cur.fetchone()[0] >= 3:
                        bloqueo = datetime.now() + timedelta(minutes=5)
                        cur.execute("UPDATE usuarios_voz SET bloqueado_hasta = %s WHERE id = %s", (bloqueo, user_id))
                elif status == "OK":
                    cur.execute("UPDATE usuarios_voz SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE id = %s", (user_id,))
                
                self.conn.commit()
        except Exception as e:
            print(f"Error en login attempt log: {e}")
            self.conn.rollback()

    def get_critical_logs(self):
        """Consulta avanzada que 'bucea' en el JSONB para encontrar fallos o baja confianza."""
        if not self.conn: return []
        try:
            with self.conn.cursor() as cur:
                query = """
                SELECT u.username, l.fecha_intento, l.resultado_json
                FROM log_accesos_voz l
                JOIN usuarios_voz u ON l.usuario_id = u.id
                WHERE l.resultado_json->>'status' = 'FAIL'
                   OR (l.resultado_json->>'confianza')::float < 0.6
                ORDER BY l.fecha_intento DESC;
                """
                cur.execute(query)
                return cur.fetchall()
        except Exception as e:
            print(f"Error en consulta de auditoría: {e}")
            return []
