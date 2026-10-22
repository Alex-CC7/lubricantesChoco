from models.database import db

class CategoriaModel:

    def listar(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT idCategoria, Nombre, Descripcion, Estado, FechaActualizacion FROM categoria WHERE Estado = 1")
        result = cursor.fetchall()
        conn.close()
        return result

    def obtener(self, id):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM categoria WHERE idCategoria = %s AND Estado = 1", (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def crear(self, nombre, descripcion):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO categoria (Nombre, Descripcion, Estado) VALUES (%s, %s, 1)",
            (nombre, descripcion)
        )
        conn.commit()
        conn.close()

    def actualizar(self, id, nombre, descripcion):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE categoria SET Nombre=%s, Descripcion=%s WHERE idCategoria=%s",
            (nombre, descripcion, id)
        )
        conn.commit()
        conn.close()

    def eliminar(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE categoria SET Estado=0 WHERE idCategoria=%s", (id,))
        conn.commit()
        conn.close()
