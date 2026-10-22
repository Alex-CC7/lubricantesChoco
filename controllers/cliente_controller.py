from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.cliente_model import ClienteModel
from utils.decorators import login_required

cliente_bp = Blueprint('clientes', __name__, url_prefix='/clientes')
model = ClienteModel()

@cliente_bp.route('/')
@login_required
def index():
    clientes = model.listar()
    return render_template('clientes/index.html', clientes=clientes)

@cliente_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    # Detectar si viene desde la pantalla de nueva venta
    next_url = request.args.get('next', '')
    if request.method == 'POST':
        razon_social = request.form['razon_social']
        nit_ci       = request.form['nit_ci']
        model.crear(razon_social, nit_ci)
        flash(f'Cliente "{razon_social}" creado exitosamente', 'success')
        # Si vino de ventas, regresar a crear venta con bandera de nuevo cliente
        if request.form.get('next') == 'venta':
            return redirect(url_for('ventas.crear') + '?cliente_nuevo=1')
        return redirect(url_for('clientes.index'))
    return render_template('clientes/form.html', accion='Crear', cliente=None, next_url=next_url)

@cliente_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar(id):
    cliente = model.obtener(id)
    if not cliente:
        flash('Cliente no encontrado', 'danger')
        return redirect(url_for('clientes.index'))
    if request.method == 'POST':
        razon_social = request.form['razon_social']
        nit_ci       = request.form['nit_ci']
        model.actualizar(id, razon_social, nit_ci)
        flash('Cliente actualizado exitosamente', 'success')
        return redirect(url_for('clientes.index'))
    return render_template('clientes/form.html', accion='Editar', cliente=cliente, next_url='')

@cliente_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    model.eliminar(id)
    flash('Cliente eliminado', 'warning')
    return redirect(url_for('clientes.index'))
