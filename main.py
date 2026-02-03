import ttkbootstrap as tb
from ttkbootstrap.constants import *
from AppInventario import AppInventario
from login import LoginWindow

def main():
    root = tb.Window(themename="superhero")  # Puedes probar: flatly, darkly, cyborg, morph, vapor
    root.title("Inventario con Login y DB")
    root.geometry("1200x700")

    def on_login_success(usuario_data):
        AppInventario(root, usuario_data)

    LoginWindow(root, on_login_success)
    root.mainloop()

if __name__ == "__main__":
    main()
