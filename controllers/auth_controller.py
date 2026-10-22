from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from models.usuario_model import UsuarioModel
from models.intento_login_model import IntentoLoginModel
from utils.security import check_password, hash_password

auth_bp = Blueprint('auth', __name__)
usuario_model = UsuarioModel()
intento_model = IntentoLoginModel()

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('dashboard'))

    bloqueado_segundos = 0
    ip = request.remote_addr

    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        registro_ip = intento_model.obtener(ip)
        if intento_model.esta_bloqueado(registro_ip):
            bloqueado_segundos = int((registro_ip['bloqueado_hasta'] - datetime.now()).total_seconds()) + 1
            flash('Demasiados intentos fallidos desde este dispositivo.', 'danger')
            return render_template('auth/login.html', bloqueado_segundos=bloqueado_segundos)

        usuario = usuario_model.obtener_por_username(username)

        if usuario:
            pwd_ok = check_password(password, usuario['Password'])
            if pwd_ok:
                usuario_model.resetear_intentos(usuario['idUsuario'])
                intento_model.resetear(ip)
                session['usuario_id'] = usuario['idUsuario']
                session['nombre']     = usuario['Nombre']
                session['rol']        = usuario['Rol']
                flash('Bienvenido, ' + usuario['Nombre'], 'success')
                return redirect(url_for('dashboard'))
            else:
                usuario_model.registrar_intento_fallido(usuario['idUsuario'])

        intento_model.registrar_intento_fallido(ip)

        registro_ip_actualizado = intento_model.obtener(ip)
        if intento_model.esta_bloqueado(registro_ip_actualizado):
            bloqueado_segundos = int((registro_ip_actualizado['bloqueado_hasta'] - datetime.now()).total_seconds()) + 1
            flash('Demasiados intentos fallidos desde este dispositivo.', 'danger')
            return render_template('auth/login.html', bloqueado_segundos=bloqueado_segundos)

        flash('Usuario o contraseña incorrectos', 'danger')

    return render_template('auth/login.html', bloqueado_segundos=bloqueado_segundos)


@auth_bp.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        username = request.form['username'].strip()
        dato = request.form['dato'].strip()
        fecha_nacimiento = request.form['fecha_nacimiento']

        usuario = usuario_model.verificar_identidad(username, dato, fecha_nacimiento)

        if usuario:
            session['recuperar_id']     = usuario['idUsuario']
            session['recuperar_nombre'] = usuario['Nombre']
            return redirect(url_for('auth.recuperar_nueva'))
        else:
            flash('Los datos ingresados no coinciden con ningún usuario registrado.', 'danger')

    return render_template('auth/recuperar.html')


@auth_bp.route('/recuperar/nueva', methods=['GET', 'POST'])
def recuperar_nueva():
    if 'recuperar_id' not in session:
        flash('Primero debes verificar tu identidad.', 'danger')
        return redirect(url_for('auth.recuperar'))

    nombre = session.get('recuperar_nombre', '')

    if request.method == 'POST':
        password  = request.form['password']
        password2 = request.form['password2']

        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres.', 'danger')
        elif password != password2:
            flash('Las contraseñas no coinciden.', 'danger')
        else:
            hashed = hash_password(password)
            usuario_model.actualizar_password(session['recuperar_id'], hashed)
            session.pop('recuperar_id', None)
            session.pop('recuperar_nombre', None)
            flash(f'Contraseña actualizada correctamente, {nombre}. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/recuperar_nueva.html', nombre=nombre)


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))