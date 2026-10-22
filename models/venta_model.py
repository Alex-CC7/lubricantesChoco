from models.database import db

class VentaModel:

    def listar(self):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.idVenta, v.TotalPagar, v.Descuento, v.FechaVenta,
                   v.Estado, v.TipoVenta, v.FechaActualizacion,
                   u.Nombre as Usuario,
                   c.RazonSocial as Cliente
            FROM venta v
            JOIN usuario u ON v.idUsuario = u.idUsuario
            JOIN cliente c ON v.cliente_idClientes = c.idClientes
            WHERE v.Estado = 1
            ORDER BY v.FechaVenta DESC
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    def obtener(self, id):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT v.*, u.Nombre as Usuario, c.RazonSocial as Cliente
            FROM venta v
            JOIN usuario u ON v.idUsuario = u.idUsuario
            JOIN cliente c ON v.cliente_idClientes = c.idClientes
            WHERE v.idVenta = %s AND v.Estado = 1
        """, (id,))
        result = cursor.fetchone()
        conn.close()
        return result

    def obtener_detalle(self, id_venta):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT vd.idVenta, vd.idProducto, vd.cantidad, vd.precio,
                   p.Nombre as Producto, p.Marca
            FROM ventadetalle vd
            JOIN producto p ON vd.idProducto = p.idProducto
            WHERE vd.idVenta = %s
        """, (id_venta,))
        result = cursor.fetchall()
        conn.close()
        return result

    def crear(self, id_venta, total, descuento, fecha_venta, tipo_venta, id_usuario, cliente_id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO venta (idVenta, TotalPagar, Descuento, FechaVenta, Estado,
                TipoVenta, idUsuario, cliente_idClientes)
            VALUES (%s, %s, %s, %s, 1, %s, %s, %s)
        """, (id_venta, total, descuento, fecha_venta, tipo_venta, id_usuario, cliente_id))
        conn.commit()
        conn.close()

    def agregar_detalle(self, id_venta, id_producto, cantidad, precio):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ventadetalle (idVenta, idProducto, cantidad, precio)
            VALUES (%s, %s, %s, %s)
        """, (id_venta, id_producto, cantidad, precio))
        conn.commit()
        conn.close()

    def proximo_id(self):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COALESCE(MAX(idVenta),0)+1 FROM venta")
        result = cursor.fetchone()[0]
        conn.close()
        return result

    def eliminar(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE venta SET Estado=0 WHERE idVenta=%s", (id,))
        conn.commit()
        conn.close()

    def reporte(self, fecha_inicio=None, fecha_fin=None):
        conn = db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT v.idVenta, v.FechaVenta, v.TotalPagar, v.Descuento, v.TipoVenta,
                   u.Nombre as Usuario, c.RazonSocial as Cliente
            FROM venta v
            JOIN usuario u ON v.idUsuario = u.idUsuario
            JOIN cliente c ON v.cliente_idClientes = c.idClientes
            WHERE v.Estado = 1
        """
        params = []
        if fecha_inicio and fecha_fin:
            query += " AND DATE(v.FechaVenta) BETWEEN %s AND %s"
            params = [fecha_inicio, fecha_fin]
        query += " ORDER BY v.FechaVenta DESC"
        cursor.execute(query, params)
        result = cursor.fetchall()
        conn.close()
        return result
