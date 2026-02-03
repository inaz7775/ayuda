from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class VistaDashboard:
    def __init__(self, parent, inventario):
        self.inventario = inventario

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        self.label_total = ttk.Label(self.frame, text="Total productos: 0")
        self.label_total.pack(anchor="w")

        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def actualizar(self):
        total = self.inventario.total_productos()
        self.label_total.config(text=f"Total productos: {total}")

        top_v = self.inventario.obtener_top_mas_vendidos(5)
        nombres_v = [p.nombre for p, _ in top_v]
        cantidades_v = [c for _, c in top_v]

        self.ax1.clear()
        if nombres_v:
            self.ax1.bar(nombres_v, cantidades_v)
            self.ax1.set_title("Más vendidos")

        top_a = self.inventario.obtener_productos_mas_tiempo_sin_mover(5)
        nombres_a = [p.nombre for p, _ in top_a]
        dias_a = [d for _, d in top_a]

        self.ax2.clear()
        if nombres_a:
            self.ax2.bar(nombres_a, dias_a, color="orange")
            self.ax2.set_title("Más tiempo sin moverse")

        self.fig.tight_layout()
        self.canvas.draw()
