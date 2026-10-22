from flask import Blueprint, render_template, request, send_file
from models.venta_model import VentaModel
from models.producto_model import ProductoModel
from models.categoria_model import CategoriaModel
from models.cliente_model import ClienteModel
from models.usuario_model import UsuarioModel
from utils.decorators import login_required
from utils.reportes import (
    generar_excel_ventas, generar_pdf_ventas,
    generar_excel_productos, generar_pdf_productos,
    generar_excel_categorias, generar_pdf_categorias,
    generar_excel_clientes, generar_pdf_clientes,
    generar_excel_usuarios, generar_pdf_usuarios,
)

reporte_bp     = Blueprint('reportes', __name__, url_prefix='/reportes')
venta_model    = VentaModel()
producto_model = ProductoModel()
cat_model      = CategoriaModel()
cli_model      = ClienteModel()
usu_model      = UsuarioModel()

# ── Ventas ──────────────────────────────────────────────
@reporte_bp.route('/ventas')
@login_required
def reporte_ventas():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin    = request.args.get('fecha_fin')
    ventas = venta_model.reporte(fecha_inicio, fecha_fin)
    return render_template('reportes/ventas.html', ventas=ventas,
                           fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)

@reporte_bp.route('/ventas/excel')
@login_required
def excel_ventas():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin    = request.args.get('fecha_fin')
    ventas = venta_model.reporte(fecha_inicio, fecha_fin)
    return send_file(generar_excel_ventas(ventas), as_attachment=True, download_name='ventas.xlsx')

@reporte_bp.route('/ventas/pdf')
@login_required
def pdf_ventas():
    fecha_inicio = request.args.get('fecha_inicio')
    fecha_fin    = request.args.get('fecha_fin')
    ventas = venta_model.reporte(fecha_inicio, fecha_fin)
    return send_file(generar_pdf_ventas(ventas), as_attachment=True, download_name='ventas.pdf')

# ── Productos ────────────────────────────────────────────
@reporte_bp.route('/productos')
@login_required
def reporte_productos():
    productos = producto_model.listar()
    return render_template('reportes/productos.html', productos=productos)

@reporte_bp.route('/productos/excel')
@login_required
def excel_productos():
    return send_file(generar_excel_productos(producto_model.listar()),
                     as_attachment=True, download_name='productos.xlsx')

@reporte_bp.route('/productos/pdf')
@login_required
def pdf_productos():
    return send_file(generar_pdf_productos(producto_model.listar()),
                     as_attachment=True, download_name='productos.pdf')

# ── Categorías ───────────────────────────────────────────
@reporte_bp.route('/categorias/excel')
@login_required
def excel_categorias():
    return send_file(generar_excel_categorias(cat_model.listar()),
                     as_attachment=True, download_name='categorias.xlsx')

@reporte_bp.route('/categorias/pdf')
@login_required
def pdf_categorias():
    return send_file(generar_pdf_categorias(cat_model.listar()),
                     as_attachment=True, download_name='categorias.pdf')

# ── Clientes ─────────────────────────────────────────────
@reporte_bp.route('/clientes/excel')
@login_required
def excel_clientes():
    return send_file(generar_excel_clientes(cli_model.listar()),
                     as_attachment=True, download_name='clientes.xlsx')

@reporte_bp.route('/clientes/pdf')
@login_required
def pdf_clientes():
    return send_file(generar_pdf_clientes(cli_model.listar()),
                     as_attachment=True, download_name='clientes.pdf')

# ── Usuarios ─────────────────────────────────────────────
@reporte_bp.route('/usuarios/excel')
@login_required
def excel_usuarios():
    return send_file(generar_excel_usuarios(usu_model.listar()),
                     as_attachment=True, download_name='usuarios.xlsx')

@reporte_bp.route('/usuarios/pdf')
@login_required
def pdf_usuarios():
    return send_file(generar_pdf_usuarios(usu_model.listar()),
                     as_attachment=True, download_name='usuarios.pdf')
