from flask import Flask, render_template, request, redirect, url_for, session
from flask_babel import Babel, _
import sqlite3
from datetime import datetime

# --- Configuración inicial ---
app = Flask(__name__)
app.secret_key = "clave_secreta"

# --- Configuración de Babel ---
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_SUPPORTED_LOCALES'] = ['es', 'en']
app.config['BABEL_TRANSLATION_DIRECTORIES'] = 'translations'


def get_locale():
    return session.get('lang', 'es')

babel = Babel(app, locale_selector=get_locale)


# --- Cambio de idioma ---
@app.route('/cambiar_idioma/<lang>')
def cambiar_idioma(lang):
    if lang in ['es', 'en']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


@app.context_processor
def inject_lang():
    return {'lang': str(get_locale())}


@app.context_processor
def inject_datetime():
    now = datetime.now()
    return {
        'fecha': now.strftime("%d/%m/%Y"),
        'hora': now.strftime("%H:%M:%S")
    }

# ==========================================================
# 🏠 PÁGINA PRINCIPAL
# ==========================================================
@app.route('/')
def index():
    fecha = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    lang = str(get_locale())
    return render_template("index.html", fecha=fecha, hora=hora, lang=lang)

# ==========================================================
# 🗄️ BASE DE DATOS
# ==========================================================
def crear_tablas():
    conexion = sqlite3.connect("viajes.db")
    cursor = conexion.cursor()

    # Tabla clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            dni TEXT PRIMARY KEY,
            password TEXT,
            nombre TEXT,
            apellido TEXT,
            telefono TEXT,
            cuenta_pago TEXT
        )
    """)

    # Tabla conductores
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conductores (
            dni TEXT PRIMARY KEY,
            password TEXT,
            nombre TEXT,
            telefono TEXT,
            vehiculo TEXT,
            metodo_pago TEXT
        )
    """)

    # Tabla viajes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS viajes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dni_cliente TEXT,
            dni_conductor TEXT,
            fecha TEXT,
            hora TEXT,
            estado TEXT DEFAULT 'pendiente'
        )
    """)

    conexion.commit()
    conexion.close()

crear_tablas()


# ==========================================================
# 👤 SECCIÓN CLIENTE
# ==========================================================
@app.route('/cliente/registro', methods=['GET', 'POST'])
def cliente_registro():
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        telefono = request.form['telefono']
        cuenta_pago = request.form['cuenta_pago']

        conexion = sqlite3.connect("viajes.db")
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO clientes VALUES (?, ?, ?, ?, ?, ?)",
                           (dni, password, nombre, apellido, telefono, cuenta_pago))
            conexion.commit()
            conexion.close()
            return redirect(url_for('cliente_login'))
        except:
            conexion.close()
            return "⚠️ DNI ya registrado."
    return render_template('cliente/cliente_registro.html')


@app.route('/cliente/login', methods=['GET', 'POST'])
def cliente_login():
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']
        conexion = sqlite3.connect("viajes.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM clientes WHERE dni=? AND password=?", (dni, password))
        cliente = cursor.fetchone()
        conexion.close()

        if cliente:
            session['cliente_dni'] = dni
            return redirect(url_for('cliente_menu'))
        else:
            return "❌ DNI o contraseña incorrectos."
    return render_template('cliente/cliente_login.html')


@app.route('/cliente/menu')
def cliente_menu():
    if 'cliente_dni' not in session:
        return redirect(url_for('cliente_login'))
    return render_template('cliente/cliente_menu.html')


@app.route('/cliente/viaje', methods=['GET', 'POST'])
def cliente_viaje():
    if 'cliente_dni' not in session:
        return redirect(url_for('cliente_login'))

    dni = session['cliente_dni']

    if request.method == 'POST':
        fecha = request.form['fecha']
        hora = request.form['hora']
        conexion = sqlite3.connect("viajes.db")
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO viajes (dni_cliente, fecha, hora) VALUES (?, ?, ?)", (dni, fecha, hora))
        conexion.commit()
        conexion.close()
        return redirect(url_for('cliente_menu'))

    return render_template('cliente/cliente_viaje.html')


@app.route('/cliente/ver_viajes')
def cliente_ver_viajes():
    if 'cliente_dni' not in session:
        return redirect(url_for('cliente_login'))

    dni = session['cliente_dni']
    conexion = sqlite3.connect("viajes.db")
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM viajes WHERE dni_cliente=?", (dni,))
    viajes = cursor.fetchall()
    conexion.close()

    viajes_traducidos = []
    for v in viajes:
        id_viaje, dni_cliente, dni_conductor, fecha, hora, estado = v
        if estado == 'pendiente':
            estado_traducido = _("pending")
        elif estado == 'completado':
            estado_traducido = _("completed")
        elif estado == 'cancelado':
            estado_traducido = _("cancelled")
        else:
            estado_traducido = estado
        viajes_traducidos.append((id_viaje, dni_cliente, dni_conductor, fecha, hora, estado_traducido))

    return render_template('cliente/cliente_ver_viajes.html', viajes=viajes_traducidos)


@app.route('/cliente/cancelar/<int:id>')
def cliente_cancelar(id):
    conexion = sqlite3.connect("viajes.db")
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM viajes WHERE id=?", (id,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('cliente_ver_viajes'))


# ==========================================================
# 🚗 SECCIÓN CONDUCTOR
# ==========================================================
@app.route('/conductor/registro', methods=['GET', 'POST'])
def conductor_registro():
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        vehiculo = request.form['vehiculo']
        metodo_pago = request.form['metodo_pago']

        conexion = sqlite3.connect("viajes.db")
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO conductores VALUES (?, ?, ?, ?, ?, ?)",
                           (dni, password, nombre, telefono, vehiculo, metodo_pago))
            conexion.commit()
            conexion.close()
            return redirect(url_for('conductor_login'))
        except:
            conexion.close()
            return "⚠️ DNI ya registrado."
    return render_template('conductor/conductor_registro.html')


@app.route('/conductor/login', methods=['GET', 'POST'])
def conductor_login():
    if request.method == 'POST':
        dni = request.form['dni']
        password = request.form['password']
        conexion = sqlite3.connect("viajes.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM conductores WHERE dni=? AND password=?", (dni, password))
        conductor = cursor.fetchone()
        conexion.close()

        if conductor:
            session['conductor_dni'] = dni
            return redirect(url_for('conductor_menu'))
        else:
            return "❌ DNI o contraseña incorrectos."
    return render_template('conductor/conductor_login.html')


@app.route('/conductor/menu')
def conductor_menu():
    if 'conductor_dni' not in session:
        return redirect(url_for('conductor_login'))
    return render_template('conductor/conductor_menu.html')


# ==========================================================
# 🔚 EJECUCIÓN
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)
