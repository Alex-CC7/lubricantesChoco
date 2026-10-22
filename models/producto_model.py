from models.database import db

class ProductoModel:

    def listar(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.idProducto, p.Nombre, p.Marca, p.Stock,
                   p.PrecioVenta, p.Estado, p.NombreProveedor, p.NroProveedor,
                   p.FechaActualizacion, cat.Nombre as Categoria
            FROM producto p
            JOIN categoria cat ON p.Categoria_idCategoria = cat.idCategoria
            WHERE p.Estado = 1
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    def obtener(self, id):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM producto WHERE idProducto = %s AND Estado = 1", (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def crear(self, nombre, marca, stock, precio_venta, nombre_proveedor, nro_proveedor, categoria_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO producto (Nombre, Marca, Stock, PrecioVenta, Estado,
                NombreProveedor, NroProveedor, Categoria_idCategoria)
            VALUES (%s, %s, %s, %s, 1, %s, %s, %s)
        """, (nombre, marca, stock, precio_venta, nombre_proveedor, nro_proveedor, categoria_id))
        conn.commit()
        conn.close()

    def actualizar(self, id, nombre, marca, stock, precio_venta, nombre_proveedor, nro_proveedor, categoria_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE producto SET Nombre=%s, Marca=%s, Stock=%s,
                PrecioVenta=%s, NombreProveedor=%s, NroProveedor=%s,
                Categoria_idCategoria=%s
            WHERE idProducto=%s
        """, (nombre, marca, stock, precio_venta, nombre_proveedor, nro_proveedor, categoria_id, id))
        conn.commit()
        conn.close()

    def eliminar(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE producto SET Estado=0 WHERE idProducto=%s", (id,))
        conn.commit()
        conn.close()
