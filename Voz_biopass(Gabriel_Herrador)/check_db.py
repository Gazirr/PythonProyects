from src.conexion_db import ConexionDB
import psycopg

def test_db():
    print("Iniciando diagnóstico de Base de Datos...")
    db = ConexionDB()
    conn = db.get_connection()
    
    if not conn:
        print("❌ ERROR: No se pudo conectar a la base de datos. Verifica el usuario/contraseña en src/config.py")
        return

    print("✅ Conexión establecida correctamente.")
    
    try:
        with conn.cursor() as cur:
            # Verificar si existen las tablas
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name IN ('usuarios_voz', 'log_accesos_voz')
            """)
            tables = [row[0] for row in cur.fetchall()]
            
            if 'usuarios_voz' in tables:
                print("✅ Tabla 'usuarios_voz' encontrada.")
                cur.execute("SELECT COUNT(*) FROM usuarios_voz")
                print(f"   Número de usuarios registrados: {cur.fetchone()[0]}")
            else:
                print("❌ ERROR: La tabla 'usuarios_voz' NO existe. ¿Has ejecutado el script SQL?")
            
            if 'log_accesos_voz' in tables:
                print("✅ Tabla 'log_accesos_voz' encontrada.")
            else:
                print("❌ ERROR: La tabla 'log_accesos_voz' NO existe.")

    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")
    finally:
        db.close_connection()

if __name__ == "__main__":
    test_db()
