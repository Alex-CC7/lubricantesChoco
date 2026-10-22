from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from models.venta_model import VentaModel
from models.producto_model import ProductoModel
from models.cliente_model import ClienteModel
from utils.decorators import login_required
from utils.reportes import generar_pdf_venta

venta_bp = Blueprint('ventas', __name__, url_prefix='/ventas')
model = VentaModel()
producto_model = ProductoModel()
cliente_model = ClienteModel()

@venta_bp.route('/')
@login_required
def index():
    ventas = model.listar()
    return render_template('ventas/index.html', ventas=ventas)

@venta_bp.route('/detalle/<int:id>')
@login_required
def detalle(id):
    venta = model.obtener(id)
    detalle = model.obtener_detalle(id)
    return render_template('ventas/detalle.html', venta=venta, detalle=detalle)

@venta_bp.route('/imprimir/<int:id>')
@login_required
def imprimir_pdf(id):
    venta   = model.obtener(id)
    detalle = model.obtener_detalle(id)
    path    = generar_pdf_venta(venta, detalle)
    return send_file(path, as_attachment=False,
                     download_name=f'venta_{id}.pdf',
                     mimetype='application/pdf')

@venta_bp.route('/crear', methods=['GET', 'POST'])
@login_required
def crear():
    productos = producto_model.listar()
    clientes  = cliente_model.listar()
    if request.method == 'POST':
        id_venta    = model.proximo_id()
        total       = request.form['total']
        descuento   = request.form['descuento']
        fecha_venta = request.form['fecha_venta']
        tipo_venta  = request.form['tipo_venta']
        cliente_id  = request.form['cliente_id']
        id_usuario  = session['usuario_id']
        model.crear(id_venta, total, descuento, fecha_venta, tipo_venta, id_usuario, cliente_id)
        for pid, cant, prec in zip(
            request.form.getlist('producto_id[]'),
            request.form.getlist('cantidad[]'),
            request.form.getlist('precio[]')
        ):
            model.agregar_detalle(id_venta, pid, cant, prec)
        flash('Venta registrada exitosamente', 'success')
        return redirect(url_for('ventas.index'))
    return render_template('ventas/form.html', productos=productos, clientes=clientes)

@venta_bp.route('/eliminar/<int:id>')
@login_required
def eliminar(id):
    model.eliminar(id)
    flash('Venta anulada', 'warning')
    return redirect(url_for('ventas.index'))
