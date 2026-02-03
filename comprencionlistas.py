from datetime import datetime
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class Producto:
    def __init__(self, id_producto, nombre, categoria, stock_actual=0,
                 stock_minimo=0, fecha_registro=None):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.stock_actual = stock_actual
        self.stock_minimo = stock_minimo
        self.fecha_registro = fecha_registro or datetime.now()
        self.fecha_ultima_salida = None

    def incrementar_stock(self, cantidad):
        self.stock_actual += cantidad

    def disminuir_stock(self, cantidad):
        if cantidad > self.stock_actual:
            raise ValueError("No hay suficiente stock")
        self.stock_actual -= cantidad
        self.fecha_ultima_salida = datetime.now()

    def dias_desde_ultima_salida(self):
        if not self.fecha_ultima_salida:
            return None
        return (datetime.now() - self.fecha_ultima_salida).days


class MovimientoInventario:
    def __init__(self, id_movimiento, producto, tipo, cantidad, fecha=None):
        self.id_movimiento = id_movimiento
        self.producto = producto
        self.tipo = tipo  # "ENTRADA" o "SALIDA"
        self.cantidad = cantidad
        self.fecha = fecha or datetime.now()

    def aplicar(self):
        if self.tipo == "ENTRADA":
            self.producto.incrementar_stock(self.cantidad)
        elif self.tipo == "SALIDA":
            self.producto.disminuir_stock(self.cantidad)
        else:
            raise ValueError("Tipo de movimiento inválido")


class Inventario:
    
    def __init__(self):
        self.productos = {}      # id_producto -> Producto
        self.movimientos = []    # lista de MovimientoInventario
        self._contador_mov = 1

    def agregar_producto(self, producto):
        self.productos[producto.id_producto] = producto

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

    def registrar_movimiento(self, id_producto, tipo, cantidad):
        producto = self.productos.get(id_producto)
        if not producto:
            raise ValueError("Producto no encontrado")
        mov = MovimientoInventario(self._contador_mov, producto, tipo, cantidad)
        mov.aplicar()
        self.movimientos.append(mov)
        self._contador_mov += 1

    def total_productos(self):
        return len(self.productos)

    def obtener_top_mas_vendidos(self, n=5):
        ventas_por_producto = defaultdict(int)
        for mov in self.movimientos:
            if mov.tipo == "SALIDA":
                ventas_por_producto[mov.producto.id_producto] += mov.cantidad
        ordenados = sorted(ventas_por_producto.items(),
                           key=lambda x: x[1],
                           reverse=True)
        return [(self.productos[id_p], cant) for id_p, cant in ordenados[:n]]

    def obtener_top_mas_antiguos(self, n=5):
        productos_ordenados = sorted(
            self.productos.values(),
            key=lambda p: p.fecha_registro
        )
        return productos_ordenados[:n]

# Reutilizamos las clases definidas antes:
# Producto, MovimientoInventario, Inventario

class AppInventario:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Inventario - OMT")
        self.inventario = Inventario()

        # Crear figura con dos gráficas
        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(121)  # Más vendidos
        self.ax2 = self.fig.add_subplot(122)  # Más tiempo sin moverse

        self._crear_widgets()
        self._poblar_datos_demo()
        self.actualizar_dashboard()

    def _crear_widgets(self):
        frame_main = ttk.Frame(self.root, padding=10)
        frame_main.pack(fill="both", expand=True)

        # Formulario
        frame_form = ttk.LabelFrame(frame_main, text="Producto")
        frame_form.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        self.entry_id = ttk.Entry(frame_form)
        self.entry_id.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, sticky="w")
        self.entry_nombre = ttk.Entry(frame_form)
        self.entry_nombre.grid(row=1, column=1, sticky="ew")

        ttk.Label(frame_form, text="Categoría:").grid(row=2, column=0, sticky="w")
        self.entry_categoria = ttk.Entry(frame_form)
        self.entry_categoria.grid(row=2, column=1, sticky="ew")

        ttk.Label(frame_form, text="Stock inicial:").grid(row=3, column=0, sticky="w")
        self.entry_stock = ttk.Entry(frame_form)
        self.entry_stock.grid(row=3, column=1, sticky="ew")

        btn_agregar = ttk.Button(frame_form, text="Agregar/Actualizar producto",
                                 command=self.agregar_producto)
        btn_agregar.grid(row=4, column=0, columnspan=2, pady=5)

        frame_form.columnconfigure(1, weight=1)

        # Movimientos
        frame_mov = ttk.LabelFrame(frame_main, text="Movimientos")
        frame_mov.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(frame_mov, text="ID Producto:").grid(row=0, column=0, sticky="w")
        self.entry_mov_id = ttk.Entry(frame_mov)
        self.entry_mov_id.grid(row=0, column=1, sticky="ew")

        ttk.Label(frame_mov, text="Cantidad:").grid(row=1, column=0, sticky="w")
        self.entry_mov_cant = ttk.Entry(frame_mov)
        self.entry_mov_cant.grid(row=1, column=1, sticky="ew")

        btn_entrada = ttk.Button(frame_mov, text="Entrada",
                                 command=lambda: self.registrar_movimiento("ENTRADA"))
        btn_salida = ttk.Button(frame_mov, text="Salida",
                                command=lambda: self.registrar_movimiento("SALIDA"))
        btn_entrada.grid(row=2, column=0, pady=5, sticky="ew")
        btn_salida.grid(row=2, column=1, pady=5, sticky="ew")

        frame_mov.columnconfigure(1, weight=1)

        # Tabla
        frame_tabla = ttk.LabelFrame(frame_main, text="Productos")
        frame_tabla.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)

        columnas = ("id", "nombre", "categoria", "stock", "registro")
        self.tree = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)

        # Dashboard
        frame_dash = ttk.LabelFrame(frame_main, text="Dashboard")
        frame_dash.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.label_total = ttk.Label(frame_dash, text="Total productos: 0")
        self.label_total.pack(anchor="w")

        self.canvas = FigureCanvasTkAgg(self.fig, master=frame_dash)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        frame_main.rowconfigure(2, weight=1)
        frame_main.columnconfigure(1, weight=1)

    def _poblar_datos_demo(self):
        p1 = Producto("P001", "Teclado", "Periféricos", 10)
        p2 = Producto("P002", "Mouse", "Periféricos", 20)
        p3 = Producto("P003", "Monitor", "Pantallas", 5)

        self.inventario.agregar_producto(p1)
        self.inventario.agregar_producto(p2)
        self.inventario.agregar_producto(p3)

        self.inventario.registrar_movimiento("P001", "SALIDA", 2)
        self.inventario.registrar_movimiento("P002", "SALIDA", 5)
        self.inventario.registrar_movimiento("P002", "SALIDA", 3)
        self.inventario.registrar_movimiento("P003", "ENTRADA", 2)

        self.refrescar_tabla()

    def agregar_producto(self):
        id_p = self.entry_id.get().strip()
        nombre = self.entry_nombre.get().strip()
        categoria = self.entry_categoria.get().strip()
        stock_txt = self.entry_stock.get().strip() or "0"

        if not id_p or not nombre:
            messagebox.showerror("Error", "ID y Nombre son obligatorios")
            return

        try:
            stock = int(stock_txt)
        except ValueError:
            messagebox.showerror("Error", "Stock debe ser un número")
            return

        if id_p in self.inventario.productos:
            prod = self.inventario.productos[id_p]
            prod.nombre = nombre
            prod.categoria = categoria
            prod.stock_actual = stock
        else:
            prod = Producto(id_p, nombre, categoria, stock)
            self.inventario.agregar_producto(prod)

        self.refrescar_tabla()
        self.actualizar_dashboard()

    def registrar_movimiento(self, tipo):
        id_p = self.entry_mov_id.get().strip()
        cant_txt = self.entry_mov_cant.get().strip()

        if not id_p or not cant_txt:
            messagebox.showerror("Error", "ID y Cantidad son obligatorios")
            return

        try:
            cant = int(cant_txt)
        except ValueError:
            messagebox.showerror("Error", "Cantidad debe ser un número")
            return

        try:
            self.inventario.registrar_movimiento(id_p, tipo, cant)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        self.refrescar_tabla()
        self.actualizar_dashboard()

    def refrescar_tabla(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for p in self.inventario.productos.values():
            self.tree.insert(
                "", "end",
                values=(
                    p.id_producto,
                    p.nombre,
                    p.categoria,
                    p.stock_actual,
                    p.fecha_registro.strftime("%Y-%m-%d %H:%M")
                )
            )

    def actualizar_dashboard(self):
    # Total productos
        total = self.inventario.total_productos()
        self.label_total.config(text=f"Total productos: {total}")

    # --- Gráfica 1: Top más vendidos ---
        top_vendidos = self.inventario.obtener_top_mas_vendidos(5)
        nombres_v = [p.nombre for p, _ in top_vendidos]
        cantidades_v = [c for _, c in top_vendidos]

        self.ax1.clear()
        if nombres_v:
            self.ax1.bar(nombres_v, cantidades_v, color="steelblue")
            self.ax1.set_title("Más vendidos")
            self.ax1.set_ylabel("Cantidad salida")
            self.ax1.tick_params(axis='x', rotation=45)
        else:
            self.ax1.text(0.5, 0.5, "Sin datos", ha="center", va="center")

    # --- Gráfica 2: Más tiempo sin moverse ---
        top_antiguos = self.inventario.obtener_productos_mas_tiempo_sin_mover(5)
        nombres_a = [p.nombre for p, _ in top_antiguos]
        dias_a = [d for _, d in top_antiguos]

        self.ax2.clear()
        if nombres_a:
            self.ax2.bar(nombres_a, dias_a, color="darkorange")
            self.ax2.set_title("Más tiempo sin moverse")
            self.ax2.set_ylabel("Días sin movimiento")
            self.ax2.tick_params(axis='x', rotation=45)
        else:
            self.ax2.text(0.5, 0.5, "Sin datos", ha="center", va="center")

        self.fig.tight_layout()
        self.canvas.draw()



if __name__ == "__main__":
    root = tk.Tk()
    app = AppInventario(root)
    root.mainloop()

    

    



#Separar por pestañas movimientos y lista de productos juntos, agregar productos, dasboard, registro de ventas