from models.database import db
from datetime import datetime

class UsuarioModel:

    def listar(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT idUsuario, Nombre, PrimerApellido, SegundoApellido, CI,
                   NroCelular, FechaNacimiento, NombreUsuario, Rol, Estado, FechaActualizacion
            FROM usuario WHERE Estado = 1
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    def obtener(self, id):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario WHERE idUsuario = %s AND Estado = 1", (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def obtener_por_username(self, username):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        # LOWER() para búsqueda case-insensitive
        # ORDER BY + LIMIT 1 asegura que siempre se tome el MISMO registro
        # aunque existan usuarios duplicados con el mismo NombreUsuario
        cursor.execute(
            "SELECT * FROM usuario WHERE LOWER(NombreUsuario) = LOWER(%s) AND Estado = 1 ORDER BY idUsuario ASC LIMIT 1",
            (username,)
        )
        result = cursor.fetchone()
        conn.close()
        return result

    def crear(self, nombre, primer_apellido, segundo_apellido, ci, nro_celular,
              fecha_nac, username, password, rol):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO usuario (Nombre, PrimerApellido, SegundoApellido, CI, NroCelular,
                FechaNacimiento, NombreUsuario, Password, Rol, Estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
        """, (nombre, primer_apellido, segundo_apellido, ci, nro_celular,
              fecha_nac, username, password, rol))
        conn.commit()
        conn.close()

    def actualizar(self, id, nombre, primer_apellido, segundo_apellido, ci,
                   nro_celular, fecha_nac, username, rol):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuario SET Nombre=%s, PrimerApellido=%s, SegundoApellido=%s,
                CI=%s, NroCelular=%s, FechaNacimiento=%s, NombreUsuario=%s, Rol=%s
            WHERE idUsuario=%s
        """, (nombre, primer_apellido, segundo_apellido, ci, nro_celular,
              fecha_nac, username, rol, id))
        conn.commit()
        conn.close()

    def actualizar_password(self, id, password):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET Password=%s WHERE idUsuario=%s", (password, id))
        conn.commit()
        conn.close()

    def verificar_identidad(self, username, dato, fecha_nacimiento):
        """
        Verifica que el usuario exista y que 'dato' coincida con su CI
        o con su NroCelular, y que la FechaNacimiento coincida también.
        """
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT * FROM usuario
            WHERE LOWER(NombreUsuario) = LOWER(%s)
              AND Estado = 1
              AND (CI = %s OR NroCelular = %s)
              AND FechaNacimiento = %s
            ORDER BY idUsuario ASC LIMIT 1
        """, (username, dato, dato, fecha_nacimiento))
        result = cursor.fetchone()
        conn.close()
        return result
        
        

    def eliminar(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET Estado=0 WHERE idUsuario=%s", (id,))
        conn.commit()
        conn.close()

    def registrar_intento_fallido(self, idUsuario):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET intentos_fallidos = intentos_fallidos + 1 WHERE idUsuario = %s",
            (idUsuario,)
        )
        conn.commit()
        cursor.execute(
            "SELECT intentos_fallidos FROM usuario WHERE idUsuario = %s", (idUsuario,)
        )
        intentos = cursor.fetchone()[0]
        if intentos >= 3:
            cursor.execute(
                "UPDATE usuario SET bloqueado_hasta = DATE_ADD(NOW(), INTERVAL 90 SECOND) WHERE idUsuario = %s",
                (idUsuario,)
            )
            conn.commit()
        conn.close()

    def resetear_intentos(self, idUsuario):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE usuario SET intentos_fallidos = 0, bloqueado_hasta = NULL WHERE idUsuario = %s",
            (idUsuario,)
        )
        conn.commit()
        conn.close()

    def esta_bloqueado(self, usuario):
        return usuario.get('bloqueado_hasta') is not None and usuario['bloqueado_hasta'] > datetime.now()