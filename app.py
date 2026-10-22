from flask import Flask, render_template, redirect, url_for, session
from controllers.auth_controller import auth_bp
from controllers.categoria_controller import categoria_bp
from controllers.cliente_controller import cliente_bp
from controllers.producto_controller import producto_bp
from controllers.usuario_controller import usuario_bp
from controllers.venta_controller import venta_bp
from controllers.reporte_controller import reporte_bp
from models.categoria_model import CategoriaModel
from models.cliente_model import ClienteModel
from models.producto_model import ProductoModel
from models.usuario_model import UsuarioModel
from models.venta_model import VentaModel
from utils.decorators import login_required
import os

app = Flask(
    __name__,
    template_folder='views/templates',
    static_folder='views/static'
)
app.secret_key = 'bd_taller_secret_2024'

# Registrar blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(reporte_bp)

# Filtro enumerate para Jinja2
def do_enumerate(iterable, start=0):
    return enumerate(iterable, start)

app.jinja_env.filters['enumerate'] = do_enumerate

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    cat_model = CategoriaModel()
    cli_model = ClienteModel()
    pro_model = ProductoModel()
    usu_model = UsuarioModel()
    ven_model = VentaModel()

    total_categorias = len(cat_model.listar())
    total_clientes   = len(cli_model.listar())
    total_productos  = len(pro_model.listar())
    total_usuarios   = len(usu_model.listar())
    ventas_lista     = ven_model.listar()
    total_ventas     = len(ventas_lista)
    ventas_recientes = list(enumerate(ventas_lista[:5], 1))

    return render_template('dashboard.html',
        total_categorias=total_categorias,
        total_clientes=total_clientes,
        total_productos=total_productos,
        total_usuarios=total_usuarios,
        total_ventas=total_ventas,
        ventas_recientes=ventas_recientes
    )

if __name__ == '__main__':
    app.run(debug=True, port=5000)
