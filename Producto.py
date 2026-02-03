from datetime import datetime

class Producto:
    def __init__(self, id_producto, nombre, categoria, stock_actual=0,
                 stock_minimo=0, descripcion="", marca="", color="", tallas="", fecha_registro=None):

        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo

        self.descripcion = descripcion or ""
        self.marca = marca
        self.color = color or ""
        self.tallas = tallas or ""

        self.fecha_registro = fecha_registro or datetime.now()
        self.fecha_ultima_salida = None
