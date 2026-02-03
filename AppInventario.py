from tkinter import ttk
from Inventario import Inventario
from vista_productos import VistaProductos
from vista_gestion_productos import VistaGestionProductos
from vista_movimientos import VistaMovimientos
from vista_dashboard import VistaDashboard
from vista_usuarios import VistaUsuarios


class AppInventario:
    def __init__(self, root, usuario_actual):
        self.root = root
        self.usuario_actual = usuario_actual
        self.inventario = Inventario()

        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True)

        self.vista_productos = VistaProductos(notebook, self.inventario)
        self.vista_gestion = VistaGestionProductos(notebook, self.inventario, self.actualizar)
        self.vista_movimientos = VistaMovimientos(notebook, self.inventario, self.actualizar)
        self.vista_dashboard = VistaDashboard(notebook, self.inventario)
        self.vista_usuarios = VistaUsuarios(notebook, self.usuario_actual)

        notebook.add(self.vista_productos.frame, text="Productos")
        notebook.add(self.vista_gestion.frame, text="Gestión")
        notebook.add(self.vista_movimientos.frame, text="Movimientos")
        notebook.add(self.vista_dashboard.frame, text="Dashboard")
        notebook.add(self.vista_usuarios.frame, text="Usuarios")

        self.actualizar()

    def actualizar(self):
        self.vista_productos.refrescar()
        self.vista_movimientos.refrescar()
        self.vista_dashboard.actualizar()
