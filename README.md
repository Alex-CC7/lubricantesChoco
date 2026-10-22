# BD Taller — Sistema de Gestión

Sistema MVC Python/Flask + MySQL.

## Instalación

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar BD en `models/database.py`
```python
self.host     = 'localhost'
self.user     = 'root'
self.password = 'TU_PASSWORD'
self.database = 'bd_taller'
```

### 3. Ejecutar script SQL en MySQL Workbench

### 4. Insertar primer admin (password en texto plano, se migrará)
```sql
USE bd_taller;
INSERT INTO usuario (Nombre, PrimerApellido, SegundoApellido, CI, NroCelular,
    FechaNacimiento, NombreUsuario, Password, Rol, Estado)
VALUES ('Admin','Sistema','Taller',12345678,70000000,
    '1990-01-01','admin','admin123','1',1);
```

### 5. Migrar passwords existentes a bcrypt (¡IMPORTANTE!)
```bash
python migrar_passwords.py
```
Esto convierte todos los passwords en texto plano al formato `$2b$12$...`
Solo necesita ejecutarse **una sola vez**.

### 6. Ejecutar
```bash
python app.py
# → http://localhost:5000
# Usuario: admin  |  Contraseña: admin123
```

## Funcionalidades

| Módulo        | Admin | Personal |
|---------------|:-----:|:--------:|
| Dashboard     | ✅    | ✅       |
| Categorías    | ✅    | ✅       |
| Clientes      | ✅    | ✅       |
| Productos     | ✅    | ✅       |
| Ventas        | ✅    | ✅       |
| Usuarios      | ✅    | ❌       |
| Reportes      | ✅    | ✅       |

## Características
- Login con sesiones Flask + passwords **bcrypt** (`$2b$12$...`)
- CRUD completo con eliminación lógica (Estado 1/0)
- **Buscador en tiempo real** en cada tabla
- Exportar **Excel** y **PDF** en cada módulo
- **Imprimir PDF** por venta individual (comprobante)
- Reporte ventas con filtro **BETWEEN** fechas
- Botón "Nuevo Cliente" directo desde Nueva Venta
- CSS externo `views/static/css/style.css`
- Bootstrap 5 via CDN
