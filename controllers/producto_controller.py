from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.producto_model import ProductoModel
from models.categoria_model import CategoriaModel
from utils.decorators import login_required

producto_bp = Blueprint('productos', __name__, url_prefix='/productos')
model = ProductoModel()
categoria_model = CategoriaModel()

@producto_bp.route('/')
@login_required
def index():
    productos = model.listar()
    return render_template('productos/index.html', productos=productos)

@producto_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    categorias = categoria_model.listar()
    if request.method == 'POST':
        model.crear(
            request.form['nombre'], request.form['marca'],
            request.form['stock'], request.form['precio_venta'],
            request.form['nombre_proveedor'], request.form['nro_proveedor'],
            request.form['categoria_id']
        )
        flash('Producto creado exitosamente', 'success')
        return redirect(url_for('productos.index'))
    return render_template('productos/form.html', accion='Crear', producto=None,
                           categorias=categorias)

@producto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    producto = model.obtener(id)
    categorias = categoria_model.listar()
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('productos.index'))
    if request.method == 'POST':
        model.actualizar(
            id, request.form['nombre'], request.form['marca'],
            request.form['stock'], request.form['precio_venta'],
            request.form['nombre_proveedor'], request.form['nro_proveedor'],
            request.form['categoria_id']
        )
        flash('Producto actualizado exitosamente', 'success')
        return redirect(url_for('productos.index'))
    return render_template('productos/form.html', accion='Editar', producto=producto,
                           categorias=categorias)

@producto_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    model.eliminar(id)
    flash('Producto eliminado', 'warning')
    return redirect(url_for('productos.index'))
