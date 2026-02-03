from datetime import datetime

class Producto:
    def __init__(self, id_producto, nombre, categoria, stock_actual=0,
                 stock_minimo=0, descripcion="", marca="", color="", fecha_registro=None):

        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo

        # Nuevos campos
        self.descripcion = descripcion or ""
        self.marca = marca
        self.color = color or ""

        self.fecha_registro = fecha_registro or datetime.now()
        self.fecha_ultima_salida = None

    def incrementar_stock(self, cantidad):
        self.stock_actual += cantidad

    def disminuir_stock(self, cantidad):
        if cantidad > self.stock_actual:
            raise ValueError("No hay suficiente stock")
        self.stock_actual -= cantidad
        self.fecha_ultima_salida = datetime.now()
