from collections import defaultdict
from datetime import datetime
from Producto import Producto
from MovimientoInventario import MovimientoInventario
from database import get_connection


class Inventario:
    def __init__(self):
        pass

    def agregar_producto(self, producto: Producto):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        INSERT OR REPLACE INTO productos
        (id, nombre, categoria, marca, descripcion, color, tallas, stock, fecha_registro)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            producto.id_producto,
            producto.nombre,
            producto.categoria,
            producto.marca,
            producto.descripcion,
            producto.color,
            producto.tallas,
            producto.stock_actual,
            producto.fecha_registro.strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()
        conn.close()

    def eliminar_producto(self, id_producto):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
        conn.commit()
        conn.close()

    def modificar_producto(self, id_producto, nombre, categoria, stock,
                           descripcion, marca, color, tallas):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        UPDATE productos
        SET nombre = ?, categoria = ?, stock = ?, descripcion = ?, marca = ?, color = ?, tallas = ?
        WHERE id = ?
        """, (nombre, categoria, stock, descripcion, marca, color, tallas, id_producto))
        conn.commit()
        conn.close()

    def obtener_productos(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT id, nombre, categoria, marca, descripcion, color, tallas, stock, fecha_registro
        FROM productos
        """)
        rows = cur.fetchall()
        conn.close()
        productos = []
        for r in rows:
            p = Producto(
                id_producto=r[0],
                nombre=r[1],
                categoria=r[2],
                stock_actual=r[7],
                descripcion=r[4],
                marca=r[3],
                color=r[5],
                tallas=r[6],
                fecha_registro=datetime.strptime(r[8], "%Y-%m-%d %H:%M:%S")
            )
            productos.append(p)
        return productos

    def registrar_movimiento(self, id_producto, tipo, cantidad):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT stock FROM productos WHERE id = ?", (id_producto,))
        row = cur.fetchone()
        if not row:
            conn.close()
            raise ValueError("Producto no encontrado")

        stock_actual = row[0]
        if tipo == "ENTRADA":
            nuevo_stock = stock_actual + cantidad
        else:
            if cantidad > stock_actual:
                conn.close()
                raise ValueError("No hay suficiente stock")
            nuevo_stock = stock_actual - cantidad

        cur.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, id_producto))

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
        INSERT INTO movimientos (id_producto, tipo, cantidad, fecha)
        VALUES (?, ?, ?, ?)
        """, (id_producto, tipo, cantidad, fecha))

        conn.commit()
        conn.close()

    def obtener_historial(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT id, id_producto, tipo, cantidad, fecha
        FROM movimientos
        ORDER BY fecha DESC
        """)
        rows = cur.fetchall()
        conn.close()
        movs = []
        for r in rows:
            m = MovimientoInventario(
                id_movimiento=r[0],
                id_producto=r[1],
                tipo=r[2],
                cantidad=r[3],
                fecha=datetime.strptime(r[4], "%Y-%m-%d %H:%M:%S")
            )
            movs.append(m)
        return movs

    def total_productos(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM productos")
        total = cur.fetchone()[0]
        conn.close()
        return total

    def obtener_top_mas_vendidos(self, n=5):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT id_producto, SUM(cantidad) as total
        FROM movimientos
        WHERE tipo = 'SALIDA'
        GROUP BY id_producto
        ORDER BY total DESC
        LIMIT ?
        """, (n,))
        rows = cur.fetchall()
        conn.close()

        productos = self.obtener_productos()
        mapa = {p.id_producto: p for p in productos}
        resultado = []
        for id_p, cant in rows:
            if id_p in mapa:
                resultado.append((mapa[id_p], cant))
        return resultado

    def obtener_productos_mas_tiempo_sin_mover(self, n=5):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
        SELECT p.id, p.nombre, p.categoria, p.marca, p.descripcion, p.color, p.tallas,
               p.stock, p.fecha_registro,
               MAX(m.fecha) as ultima_salida
        FROM productos p
        LEFT JOIN movimientos m
            ON p.id = m.id_producto AND m.tipo = 'SALIDA'
        GROUP BY p.id
        """)
        rows = cur.fetchall()
        conn.close()

        lista = []
        now = datetime.now()
        for r in rows:
            fecha_reg = datetime.strptime(r[8], "%Y-%m-%d %H:%M:%S")
            if r[9]:
                ultima = datetime.strptime(r[9], "%Y-%m-%d %H:%M:%S")
            else:
                ultima = fecha_reg
            dias = (now - ultima).days
            p = Producto(
                id_producto=r[0],
                nombre=r[1],
                categoria=r[2],
                stock_actual=r[7],
                descripcion=r[4],
                marca=r[3],
                color=r[5],
                tallas=r[6],
                fecha_registro=fecha_reg
            )
            lista.append((p, dias))

        lista.sort(key=lambda x: x[1], reverse=True)
        return lista[:n]
