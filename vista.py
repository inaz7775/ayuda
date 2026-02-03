from tkinter import ttk, messagebox
from Producto import Producto

class VistaProductos:
    def __init__(self, parent, inventario, callback_actualizar):
        self.inventario = inventario
        self.callback_actualizar = callback_actualizar

        frame = ttk.Frame(parent)
        frame.pack(fill="both", expand=True)

        # Formulario
        ttk.Label(frame, text="ID:").grid(row=0, column=0)
        self.entry_id = ttk.Entry(frame)
        self.entry_id.grid(row=0, column=1)

        ttk.Label(frame, text="Nombre:").grid(row=1, column=0)
        self.entry_nombre = ttk.Entry(frame)
        self.entry_nombre.grid(row=1, column=1)

        ttk.Label(frame, text="Categoría:").grid(row=2, column=0)
        self.entry_categoria = ttk.Entry(frame)
        self.entry_categoria.grid(row=2, column=1)

        ttk.Label(frame, text="Stock inicial:").grid(row=3, column=0)
        self.entry_stock = ttk.Entry(frame)
        self.entry_stock.grid(row=3, column=1)

        ttk.Button(frame, text="Agregar", command=self.agregar_producto).grid(row=4, column=0, columnspan=2)

        # Tabla
        columnas = ("id", "nombre", "categoria", "stock")
        self.tree = ttk.Treeview(frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=5, column=0, columnspan=2, sticky="nsew")

        frame.rowconfigure(5, weight=1)
        frame.columnconfigure(1, weight=1)

    def agregar_producto(self):
        id_p = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.entry_categoria.get().strip()
        stock = int(self.entry_stock.get().strip() or 0)

        prod = Producto(id_p, nombre, categoria, stock)
        self.inventario.agregar_producto(prod)

        self.callback_actualizar()  # refresca dashboard
        self.refrescar_tabla()

    def refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.inventario.productos.values():
            self.tree.insert("", "end", values=(p.id_producto, p.nombre, p.categoria, p.stock_actual))
