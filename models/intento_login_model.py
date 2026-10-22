from models.database import db
from datetime import datetime

class IntentoLoginModel:

    def obtener(self, ip):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM intentos_login WHERE ip = %s", (ip,))
        result = cursor.fetchone()
        conn.close()
        return result

    def registrar_intento_fallido(self, ip):
        conn = db.get_connection()
        cursor = conn.cursor()
        # INSERT ... ON DUPLICATE KEY: crea la fila si es la primera vez que esa IP falla,
        # o incrementa el contador si ya existe.
        cursor.execute("""
            INSERT INTO intentos_login (ip, intentos, bloqueado_hasta)
            VALUES (%s, 1, NULL)
            ON DUPLICATE KEY UPDATE intentos = intentos + 1
        """, (ip,))
        conn.commit()

        cursor.execute("SELECT intentos FROM intentos_login WHERE ip = %s", (ip,))
        intentos = cursor.fetchone()[0]

        if intentos >= 3:
            cursor.execute(
                "UPDATE intentos_login SET bloqueado_hasta = DATE_ADD(NOW(), INTERVAL 90 SECOND) WHERE ip = %s",
                (ip,)
            )
            conn.commit()
        conn.close()

    def resetear(self, ip):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE intentos_login SET intentos = 0, bloqueado_hasta = NULL WHERE ip = %s",
            (ip,)
        )
        conn.commit()
        conn.close()

    def esta_bloqueado(self, registro):
        if not registro:
            return False
        return registro.get('bloqueado_hasta') is not None and registro['bloqueado_hasta'] > datetime.now()