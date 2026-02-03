from datetime import datetime

class MovimientoInventario:
    def __init__(self, id_movimiento, id_producto, tipo, cantidad, fecha=None):
        self.id_movimiento = id_movimiento
        self.id_producto = id_producto
        self.tipo = tipo
        self.cantidad = cantidad
        self.fecha = fecha or datetime.now()
