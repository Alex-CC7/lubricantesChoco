"""
Ejecutar UNA SOLA VEZ para hashear los passwords existentes en texto plano.
    python migrar_passwords.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from models.database import db
from utils.security import hash_password

def es_ya_hasheado(pwd: str) -> bool:
    return pwd.startswith('$2a$') or pwd.startswith('$2b$')

def migrar():
    conn   = db.get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT idUsuario, NombreUsuario, Password FROM usuario")
    usuarios = cursor.fetchall()
    actualizados = 0
    for u in usuarios:
        pwd = u['Password']
        if not es_ya_hasheado(pwd):
            nuevo_hash = hash_password(pwd)
            upd = conn.cursor()
            upd.execute("UPDATE usuario SET Password=%s WHERE idUsuario=%s",
                        (nuevo_hash, u['idUsuario']))
            conn.commit()
            print(f"  ✔ {u['NombreUsuario']} — migrado")
            actualizados += 1
        else:
            print(f"  ○ {u['NombreUsuario']} — ya hasheado, omitido")
    conn.close()
    print(f"\nListo: {actualizados} password(s) migrado(s).")

if __name__ == '__main__':
    migrar()
