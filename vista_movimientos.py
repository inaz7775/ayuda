from tkinter import ttk, messagebox

class VistaMovimientos:
    def __init__(self, parent, inventario, callback):
        self.inventario = inventario
        self.callback = callback

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        ttk.Label(self.frame, text="ID Producto:").grid(row=0, column=0)
        self.e_id = ttk.Entry(self.frame)
        self.e_id.grid(row=0, column=1)

        ttk.Label(self.frame, text="Cantidad:").grid(row=1, column=0)
        self.e_cant = ttk.Entry(self.frame)
        self.e_cant.grid(row=1, column=1)

        ttk.Button(self.frame, text="Entrada", command=lambda: self.registrar("ENTRADA")).grid(row=2, column=0)
        ttk.Button(self.frame, text="Salida", command=lambda: self.registrar("SALIDA")).grid(row=2, column=1)

        columnas = ("id", "id_producto", "tipo", "cantidad", "fecha")
        self.tree = ttk.Treeview(self.frame, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
        self.tree.grid(row=3, column=0, columnspan=2, sticky="nsew")

        self.frame.rowconfigure(3, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.refrescar()

    def registrar(self, tipo):
        try:
            self.inventario.registrar_movimiento(
                self.e_id.get(),
                tipo,
                int(self.e_cant.get())
            )
            self.callback()
            self.refrescar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for mov in self.inventario.obtener_historial():
            self.tree.insert("", "end", values=(
                mov.id_movimiento,
                mov.id_producto,
                mov.tipo,
                mov.cantidad,
                mov.fecha.strftime("%Y-%m-%d %H:%M")
            ))
