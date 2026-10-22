from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.usuario_model import UsuarioModel
from utils.decorators import login_required, admin_required
from utils.security import hash_password

usuario_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')
model = UsuarioModel()

@usuario_bp.route('/')
@login_required
@admin_required
def index():
    usuarios = model.listar()
    return render_template('usuarios/index.html', usuarios=usuarios)

@usuario_bp.route('/crear', methods=['GET', 'POST'])
@login_required
@admin_required
def crear():
    if request.method == 'POST':
        pwd_plano = request.form['password']
        if not pwd_plano:
            flash('La contraseña es obligatoria al crear un usuario', 'danger')
            return redirect(url_for('usuarios.crear'))
        model.crear(
            request.form['nombre'],
            request.form['primer_apellido'],
            request.form['segundo_apellido'],
            request.form['ci'],
            request.form['nro_celular'],
            request.form['fecha_nacimiento'],
            request.form['username'],
            hash_password(pwd_plano),   # ← hash bcrypt
            request.form['rol']
        )
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('usuarios.index'))
    return render_template('usuarios/form.html', accion='Crear', usuario=None)

@usuario_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def editar(id):
    usuario = model.obtener(id)
    if not usuario:
        flash('Usuario no encontrado', 'danger')
        return redirect(url_for('usuarios.index'))
    if request.method == 'POST':
        model.actualizar(
            id,
            request.form['nombre'],
            request.form['primer_apellido'],
            request.form['segundo_apellido'],
            request.form['ci'],
            request.form['nro_celular'],
            request.form['fecha_nacimiento'],
            request.form['username'],
            request.form['rol']
        )
        pwd_plano = request.form.get('password', '').strip()
        if pwd_plano:
            model.actualizar_password(id, hash_password(pwd_plano))  # ← hash bcrypt
            flash('Usuario actualizado (contraseña cambiada)', 'success')
        else:
            flash('Usuario actualizado', 'success')
        return redirect(url_for('usuarios.index'))
    return render_template('usuarios/form.html', accion='Editar', usuario=usuario)

@usuario_bp.route('/eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    if session.get('usuario_id') == id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('usuarios.index'))
    model.eliminar(id)
    flash('Usuario eliminado', 'warning')
    return redirect(url_for('usuarios.index'))
