from tkinter import ttk, messagebox

class VistaProductos:
    def __init__(self, parent, inventario):
        self.inventario = inventario
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, text="Buscar:").grid(row=0, column=0)
        self.entry_buscar = ttk.Entry(self.frame)
        self.entry_buscar.grid(row=0, column=1)
        ttk.Button(self.frame, text="Filtrar", command=self.filtrar).grid(row=0, column=2)

        columnas = ("id", "nombre", "categoria", "marca", "color", "stock")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")

        ttk.Button(self.frame, text="Modificar", command=self.modificar).grid(row=2, column=1)

        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.refrescar()

    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.inventario.productos.values():
            self.tree.insert("", "end", values=(
                p.id_producto, p.nombre, p.categoria, p.marca, p.color, p.stock_actual
            ))

    def filtrar(self):
        texto = self.entry_buscar.get().lower()

        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.inventario.productos.values():
            if texto in p.nombre.lower() or texto in p.categoria.lower() or texto in p.marca.lower():
                self.tree.insert("", "end", values=(
                    p.id_producto, p.nombre, p.categoria, p.marca, p.color, p.stock_actual
                ))

    def modificar(self):
        item = self.tree.selection()
        if not item:
            messagebox.showerror("Error", "Selecciona un producto")
            return

        id_p, nombre, categoria, marca, color, stock = self.tree.item(item)["values"]
        p = self.inventario.productos[id_p]

        top = ttk.Toplevel(self.frame)
        top.title("Modificar producto")

        ttk.Label(top, text="Nombre:").grid(row=0, column=0)
        e_nombre = ttk.Entry(top)
        e_nombre.insert(0, nombre)
        e_nombre.grid(row=0, column=1)

        ttk.Label(top, text="Categoría:").grid(row=1, column=0)
        e_cat = ttk.Entry(top)
        e_cat.insert(0, categoria)
        e_cat.grid(row=1, column=1)

        ttk.Label(top, text="Marca:").grid(row=2, column=0)
        e_marca = ttk.Entry(top)
        e_marca.insert(0, marca)
        e_marca.grid(row=2, column=1)

        ttk.Label(top, text="Descripción:").grid(row=3, column=0)
        e_desc = ttk.Entry(top)
        e_desc.insert(0, p.descripcion)
        e_desc.grid(row=3, column=1)

        ttk.Label(top, text="Color:").grid(row=4, column=0)
        e_color = ttk.Entry(top)
        e_color.insert(0, color)
        e_color.grid(row=4, column=1)

        ttk.Label(top, text="Stock:").grid(row=5, column=0)
        e_stock = ttk.Entry(top)
        e_stock.insert(0, stock)
        e_stock.grid(row=5, column=1)

        def guardar():
            self.inventario.modificar_producto(
                id_p,
                e_nombre.get(),
                e_cat.get(),
                int(e_stock.get()),
                e_desc.get(),
                e_marca.get(),
                e_color.get()
            )
            self.refrescar()
            top.destroy()

        ttk.Button(top, text="Guardar", command=guardar).grid(row=6, column=0, columnspan=2)
