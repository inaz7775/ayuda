import ttkbootstrap as tb
from ttkbootstrap.constants import *

from Inventario import Inventario
from vista_productos import VistaProductos
from vista_gestion_productos import VistaGestionProductos
from vista_movimientos import VistaMovimientos
from vista_dashboard import VistaDashboard


class AppInventario:
    def __init__(self, root):
        self.root = root
        self.inventario = Inventario()

        # Header
        header = tb.Frame(root, padding=10)
        header.pack(fill=X)

        titulo = tb.Label(
            header,
            text="Sistema de Inventario",
            font=("Segoe UI", 18, "bold")
        )
        titulo.pack(side=LEFT)

        subtitulo = tb.Label(
            header,
            text="Control de productos, movimientos y análisis",
            font=("Segoe UI", 10)
        )
        subtitulo.pack(side=LEFT, padx=15)

        # Notebook principal
        notebook = tb.Notebook(root, bootstyle="primary")
        notebook.pack(fill=BOTH, expand=True, padx=10, pady=(0, 10))

        self.vista_productos = VistaProductos(notebook, self.inventario)
        self.vista_gestion = VistaGestionProductos(notebook, self.inventario, self.actualizar)
        self.vista_movimientos = VistaMovimientos(notebook, self.inventario, self.actualizar)
        self.vista_dashboard = VistaDashboard(notebook, self.inventario)

        notebook.add(self.vista_productos.frame, text="📦 Productos")
        notebook.add(self.vista_gestion.frame, text="➕ Gestión")
        notebook.add(self.vista_movimientos.frame, text="🔁 Movimientos")
        notebook.add(self.vista_dashboard.frame, text="📊 Dashboard")

    def actualizar(self):
        self.vista_productos.refrescar()
        self.vista_movimientos.refrescar()
        self.vista_dashboard.actualizar()
