import ttkbootstrap as tb
from ttkbootstrap.constants import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class VistaDashboard:
    def __init__(self, parent, inventario):
        self.inventario = inventario

        self.frame = tb.Frame(parent, padding=10)
        self.frame.pack(fill=BOTH, expand=True)

        header = tb.Label(self.frame, text="Resumen general del inventario", font=("Segoe UI", 14, "bold"))
        header.pack(anchor=W, pady=(0, 10))

        self.label_total = tb.Label(self.frame, text="Total productos: 0", font=("Segoe UI", 11))
        self.label_total.pack(anchor=W, pady=(0, 10))

        self.fig = Figure(figsize=(8, 4), dpi=100)
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def actualizar(self):
        total = self.inventario.total_productos()
        self.label_total.config(text=f"Total productos: {total}")

        # Más vendidos
        top_v = self.inventario.obtener_top_mas_vendidos(5)
        nombres_v = [p.nombre for p, _ in top_v]
        cantidades_v = [c for _, c in top_v]

        self.ax1.clear()
        if nombres_v:
            self.ax1.bar(nombres_v, cantidades_v, color="#1f77b4")
            self.ax1.set_title("Top más vendidos", fontsize=10)
            self.ax1.tick_params(axis="x", rotation=45, labelsize=8)
        else:
            self.ax1.text(0.5, 0.5, "Sin datos", ha="center", va="center")

        # Más tiempo sin moverse
        top_a = self.inventario.obtener_productos_mas_tiempo_sin_mover(5)
        nombres_a = [p.nombre for p, _ in top_a]
        dias_a = [d for _, d in top_a]

        self.ax2.clear()
        if nombres_a:
            self.ax2.bar(nombres_a, dias_a, color="#ff7f0e")
            self.ax2.set_title("Más tiempo sin moverse", fontsize=10)
            self.ax2.tick_params(axis="x", rotation=45, labelsize=8)
        else:
            self.ax2.text(0.5, 0.5, "Sin datos", ha="center", va="center")

        self.fig.tight_layout()
        self.canvas.draw()
