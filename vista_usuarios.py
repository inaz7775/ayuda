import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
from database import get_connection, hash_password


class VistaUsuarios:
    def __init__(self, parent, usuario_actual):
        self.usuario_actual = usuario_actual
        self.frame = tb.Frame(parent, padding=15)
        self.frame.pack(fill="both", expand=True)

        if self.usuario_actual["rol"] != "admin":
            tb.Label(self.frame, text="Solo el administrador puede gestionar usuarios",
                     font=("Segoe UI", 12, "bold")).pack(pady=20)
            return

        title = tb.Label(self.frame, text="Gestión de Usuarios", font=("Segoe UI", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Formulario
        tb.Label(self.frame, text="Nombre:").grid(row=1, column=0, sticky="w")
        self.e_nombre = tb.Entry(self.frame, width=30)
        self.e_nombre.grid(row=1, column=1, pady=5)

        tb.Label(self.frame, text="Usuario:").grid(row=2, column=0, sticky="w")
        self.e_usuario = tb.Entry(self.frame, width=30)
        self.e_usuario.grid(row=2, column=1, pady=5)

        tb.Label(self.frame, text="Contraseña:").grid(row=3, column=0, sticky="w")
        self.e_pass = tb.Entry(self.frame, width=30, show="*")
        self.e_pass.grid(row=3, column=1, pady=5)

        tb.Label(self.frame, text="Rol:").grid(row=4, column=0, sticky="w")

        # 🔥 ComboBox con solo admin/usuario
        self.e_rol = tb.Combobox(self.frame, values=["admin", "usuario"], width=28, state="readonly")
        self.e_rol.current(1)  # por defecto "usuario"
        self.e_rol.grid(row=4, column=1, pady=5)

        tb.Button(self.frame, text="Crear Usuario", bootstyle="success",
                  command=self.crear_usuario).grid(row=5, column=0, columnspan=2, pady=15)

        # Tabla
        columnas = ("id", "nombre", "usuario", "rol")
        self.tree = tb.Treeview(self.frame, columns=columnas, show="headings", bootstyle="info")
        for col in columnas:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=150)
        self.tree.grid(row=6, column=0, columnspan=2, sticky="nsew", pady=10)

        self.frame.rowconfigure(6, weight=1)
        self.frame.columnconfigure(1, weight=1)

        self.refrescar()

    def crear_usuario(self):
        nombre = self.e_nombre.get().strip()
        usuario = self.e_usuario.get().strip()
        password = self.e_pass.get().strip()
        rol = self.e_rol.get().strip()

        if not nombre or not usuario or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("""
            INSERT INTO usuarios (nombre, usuario, password, rol)
            VALUES (?, ?, ?, ?)
            """, (nombre, usuario, hash_password(password), rol))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        conn.close()
        self.refrescar()

    def refrescar(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nombre, usuario, rol FROM usuarios")
        rows = cur.fetchall()
        conn.close()

        for r in rows:
            self.tree.insert("", "end", values=r)

