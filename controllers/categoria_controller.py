from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.categoria_model import CategoriaModel
from utils.decorators import login_required

categoria_bp = Blueprint('categorias', __name__, url_prefix='/categorias')
model = CategoriaModel()

@categoria_bp.route('/')
@login_required
def index():
    categorias = model.listar()
    return render_template('categorias/index.html', categorias=categorias)

@categoria_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        model.crear(nombre, descripcion)
        flash('Categoría creada exitosamente', 'success')
        return redirect(url_for('categorias.index'))
    return render_template('categorias/form.html', accion='Crear', categoria=None)

@categoria_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    categoria = model.obtener(id)
    if not categoria:
        flash('Categoría no encontrada', 'danger')
        return redirect(url_for('categorias.index'))
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        model.actualizar(id, nombre, descripcion)
        flash('Categoría actualizada exitosamente', 'success')
        return redirect(url_for('categorias.index'))
    return render_template('categorias/form.html', accion='Editar', categoria=categoria)

@categoria_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    model.eliminar(id)
    flash('Categoría eliminada', 'warning')
    return redirect(url_for('categorias.index'))
