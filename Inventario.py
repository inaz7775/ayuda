from collections import defaultdict
from datetime import datetime

from Producto import Producto
from MovimientoInventario import MovimientoInventario


class Inventario:
    def __init__(self):
        self.productos = {}
        self.movimientos = []
        self._contador_mov = 1

    def agregar_producto(self, producto):
        self.productos[producto.id_producto] = producto

    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]
        else:
            raise ValueError("Producto no encontrado")

    def modificar_producto(self, id_producto, nombre, categoria, stock, descripcion, marca, color):
        if id_producto not in self.productos:
            raise ValueError("Producto no encontrado")

        p = self.productos[id_producto]
        p.nombre = nombre
        p.categoria = categoria
        p.stock_actual = stock
        p.descripcion = descripcion
        p.marca = marca
        p.color = color

    def registrar_movimiento(self, id_producto, tipo, cantidad):
        if id_producto not in self.productos:
            raise ValueError("Producto no encontrado")

        producto = self.productos[id_producto]
        mov = MovimientoInventario(self._contador_mov, producto, tipo, cantidad)

        if tipo == "ENTRADA":
            producto.incrementar_stock(cantidad)
        else:
            producto.disminuir_stock(cantidad)

        self.movimientos.append(mov)
        self._contador_mov += 1

    def obtener_historial(self):
        return self.movimientos

    def total_productos(self):
        return len(self.productos)

    def obtener_top_mas_vendidos(self, n=5):
        ventas = defaultdict(int)
        for mov in self.movimientos:
            if mov.tipo == "SALIDA":
                ventas[mov.producto.id_producto] += mov.cantidad

        ordenados = sorted(ventas.items(), key=lambda x: x[1], reverse=True)
        return [(self.productos[id_p], cant) for id_p, cant in ordenados[:n]]

    def obtener_productos_mas_tiempo_sin_mover(self, n=5):
        lista = []
        for p in self.productos.values():
            if p.fecha_ultima_salida:
                dias = (datetime.now() - p.fecha_ultima_salida).days
            else:
                dias = (datetime.now() - p.fecha_registro).days
            lista.append((p, dias))

        lista.sort(key=lambda x: x[1], reverse=True)
        return lista[:n]
