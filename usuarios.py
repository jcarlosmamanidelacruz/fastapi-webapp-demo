import psycopg2
from pydantic import BaseModel, constr
from typing import Optional

# Modelo de entrada
class UsuarioIn(BaseModel):
    no_nombre: Optional[str] = None
    no_apelli: Optional[str] = None
    nu_telefo: Optional[str] = None
    pw_contra: Optional[str] = None
    co_valida: Optional[int] = None


# Función para obtener conexión a PostgreSQL
def get_connection():
    return psycopg2.connect(
        dbname="BDCAPTURAS",
        user="admin_gso",
        password="Acceso123",
        host="gsopostgresql.postgres.database.azure.com",
        port="5432"
    )

def registrar_usuario(usuario: UsuarioIn):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Ejecutar el stored procedure y obtener el JSON devuelto
        cursor.execute("""
            SELECT wfcaptur.sp_registrar_usuario(%s, %s, %s, %s)
        """, (
            usuario.no_nombre,
            usuario.no_apelli,
            usuario.nu_telefo,
            usuario.pw_contra
        ))
        conn.commit()
        # Obtener el resultado JSON (como string/dict)
        result_json = cursor.fetchone()[0]
        return result_json

    except Exception as e:
        return {
            "status": 400,
            "message": f"Error al ejecutar el stored procedure: {str(e)}",
            "data": None
        }

    finally:
        cursor.close()
        conn.close()

# ACTIVAR USUARIO

def activar_usuario(usuario: UsuarioIn):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Ejecutar el stored procedure y obtener el JSON devuelto
        cursor.execute("""
            SELECT wfcaptur.sp_activar_usuario(%s, %s)
        """, (
            usuario.nu_telefo,
            usuario.co_valida
        ))
        conn.commit()
        # Obtener el resultado JSON (como string/dict)
        result_json = cursor.fetchone()[0]
        return result_json

    except Exception as e:
        return {
            "status": 400,
            "message": f"Error al ejecutar el stored procedure: {str(e)}",
            "data": None
        }

    finally:
        cursor.close()
        conn.close()

#  REENVIAR CODIGO DE VERIFICACION

def reenviar_codigo(usuario: UsuarioIn):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Ejecutar el stored procedure y obtener el JSON devuelto
        cursor.execute("""
            SELECT wfcaptur.sp_enviar_verificacion(%s)
        """, (
            usuario.nu_telefo,
        ))
        conn.commit()
        # Obtener el resultado JSON (como string/dict)
        result_json = cursor.fetchone()[0]
        return result_json

    except Exception as e:
        return {
            "status": 400,
            "message": f"Error al ejecutar el stored procedure: {str(e)}",
            "data": None
        }

    finally:
        cursor.close()
        conn.close()
