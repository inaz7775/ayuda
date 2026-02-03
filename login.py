import tkinter as tk
from tkinter import ttk, messagebox
from database import init_db, crear_usuario_inicial, validar_login


class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.on_login_success = on_login_success

        first_time = init_db()
        if first_time:
            self._show_initial_register()
        else:
            self._show_login()

    def _show_initial_register(self):
        self.top = tk.Toplevel(self.root)
        self.top.title("Registro inicial (admin)")

        ttk.Label(self.top, text="Nombre:").grid(row=0, column=0)
        self.e_nombre = ttk.Entry(self.top)
        self.e_nombre.grid(row=0, column=1)

        ttk.Label(self.top, text="Usuario:").grid(row=1, column=0)
        self.e_usuario = ttk.Entry(self.top)
        self.e_usuario.grid(row=1, column=1)

        ttk.Label(self.top, text="Contraseña:").grid(row=2, column=0)
        self.e_pass = ttk.Entry(self.top, show="*")
        self.e_pass.grid(row=2, column=1)

        ttk.Button(self.top, text="Crear admin", command=self._crear_admin).grid(row=3, column=0, columnspan=2)

    def _crear_admin(self):
        nombre = self.e_nombre.get().strip()
        usuario = self.e_usuario.get().strip()
        password = self.e_pass.get().strip()
        if not nombre or not usuario or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        crear_usuario_inicial(nombre, usuario, password)
        self.top.destroy()
        self._show_login()

    def _show_login(self):
        self.login_frame = ttk.Frame(self.root, padding=20)
        self.login_frame.pack(expand=True)

        ttk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0)
        self.l_usuario = ttk.Entry(self.login_frame)
        self.l_usuario.grid(row=0, column=1)

        ttk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0)
        self.l_pass = ttk.Entry(self.login_frame, show="*")
        self.l_pass.grid(row=1, column=1)

        ttk.Button(self.login_frame, text="Ingresar", command=self._login).grid(row=2, column=0, columnspan=2, pady=10)

    def _login(self):
        usuario = self.l_usuario.get().strip()
        password = self.l_pass.get().strip()
        data = validar_login(usuario, password)
        if not data:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
            return
        self.login_frame.destroy()
        self.on_login_success(data)
