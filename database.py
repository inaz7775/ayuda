import sqlite3
import os
from hashlib import sha256

DB_NAME = "inventario.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    first_time = not os.path.exists(DB_NAME)
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        usuario TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        categoria TEXT NOT NULL,
        marca TEXT NOT NULL,
        descripcion TEXT,
        color TEXT,
        tallas TEXT,
        stock INTEGER NOT NULL,
        fecha_registro TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_producto TEXT NOT NULL,
        tipo TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        FOREIGN KEY (id_producto) REFERENCES productos(id)
    )
    """)

    conn.commit()
    conn.close()
    return first_time


def hash_password(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


def crear_usuario_inicial(nombre, usuario, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM usuarios")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute(
            "INSERT INTO usuarios (nombre, usuario, password, rol) VALUES (?, ?, ?, ?)",
            (nombre, usuario, hash_password(password), "admin")
        )
        conn.commit()
    conn.close()


def validar_login(usuario, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, nombre, rol, password FROM usuarios WHERE usuario = ?",
        (usuario,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    if row[3] != hash_password(password):
        return None
    return {"id": row[0], "nombre": row[1], "rol": row[2]}
