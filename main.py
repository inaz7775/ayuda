import ttkbootstrap as tb
from ttkbootstrap.constants import *
from AppInventario import AppInventario

if __name__ == "__main__":
    root = tb.Window(themename="superhero")  # prueba: cosmo, flatly, darkly, superhero, etc.
    root.title("Sistema de Inventario - OMT")
    root.geometry("1100x650")
    app = AppInventario(root)
    root.mainloop()
