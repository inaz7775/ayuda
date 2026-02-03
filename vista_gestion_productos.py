from tkinter import ttk, messagebox
from Producto import Producto

class VistaGestionProductos:
    def __init__(self, parent, inventario, callback):
        self.inventario = inventario
        self.callback = callback

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, text="ID:").grid(row=0, column=0)
        self.e_id = ttk.Entry(self.frame)
        self.e_id.grid(row=0, column=1)

        ttk.Label(self.frame, text="Nombre:").grid(row=1, column=0)
        self.e_nombre = ttk.Entry(self.frame)
        self.e_nombre.grid(row=1, column=1)

        ttk.Label(self.frame, text="Categoría:").grid(row=2, column=0)
        self.e_categoria = ttk.Entry(self.frame)
        self.e_categoria.grid(row=2, column=1)

        ttk.Label(self.frame, text="Marca:").grid(row=3, column=0)
        self.e_marca = ttk.Entry(self.frame)
        self.e_marca.grid(row=3, column=1)

        ttk.Label(self.frame, text="Descripción (opcional):").grid(row=4, column=0)
        self.e_descripcion = ttk.Entry(self.frame)
        self.e_descripcion.grid(row=4, column=1)

        ttk.Label(self.frame, text="Color (opcional):").grid(row=5, column=0)
        self.e_color = ttk.Entry(self.frame)
        self.e_color.grid(row=5, column=1)

        ttk.Label(self.frame, text="Stock:").grid(row=6, column=0)
        self.e_stock = ttk.Entry(self.frame)
        self.e_stock.grid(row=6, column=1)

        ttk.Button(self.frame, text="Agregar", command=self.agregar).grid(row=7, column=0)
        ttk.Button(self.frame, text="Eliminar", command=self.eliminar).grid(row=7, column=1)

    def agregar(self):
        p = Producto(
            self.e_id.get(),
            self.e_nombre.get(),
            self.e_categoria.get(),
            int(self.e_stock.get() or 0),
            descripcion=self.e_descripcion.get(),
            marca=self.e_marca.get(),
            color=self.e_color.get()
        )
        self.inventario.agregar_producto(p)
        self.callback()

    def eliminar(self):
        try:
            self.inventario.eliminar_producto(self.e_id.get())
            self.callback()
        except Exception as e:
            messagebox.showerror("Error", str(e))
