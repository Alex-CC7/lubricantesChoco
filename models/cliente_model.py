from models.database import db

class ClienteModel:

    def listar(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idClientes, RazonSocial, `Nit/CI`, Estado, FechaActualizacion FROM cliente WHERE Estado = 1")
        result = cursor.fetchall()
        conn.close()
        return result

    def obtener(self, id):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM cliente WHERE idClientes = %s AND Estado = 1", (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def crear(self, razon_social, nit_ci):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO cliente (RazonSocial, `Nit/CI`, Estado) VALUES (%s, %s, 1)",
            (razon_social, nit_ci)
        )
        conn.commit()
        conn.close()

    def actualizar(self, id, razon_social, nit_ci):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE cliente SET RazonSocial=%s, `Nit/CI`=%s WHERE idClientes=%s",
            (razon_social, nit_ci, id)
        )
        conn.commit()
        conn.close()

    def eliminar(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE cliente SET Estado=0 WHERE idClientes=%s", (id,))
        conn.commit()
        conn.close()
