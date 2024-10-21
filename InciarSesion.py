from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave más segura en producción

# Datos de prueba de usuarios
usuarios_validos = {
    'admin': '1234',
    'usuario': '5678'
}

@app.route('/')
def form():
    return render_template('IniciarSesion.html')

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    recordarme = request.form.get('recordarme')  # Capturamos el valor del checkbox "Recordarme"
    
    # Verificar las credenciales
    if usuario in usuarios_validos and usuarios_validos[usuario] == contrasena:
        # Guardar el usuario en la sesión
        session['usuario'] = usuario
        
        # Si el checkbox "Recordarme" está marcado, ajustar la duración de la sesión
        if recordarme:
            session.permanent = True  # Esto hace que la sesión sea permanente
            app.permanent_session_lifetime = timedelta(days=7)  # La sesión durará 7 días si se selecciona "Recordarme"
        else:
            session.permanent = False  # La sesión terminará al cerrar el navegador

        # Redirigir a la pantalla de inicio de vehículos
        return redirect(url_for('Inicio'))  # Aquí te aseguras de que la redirección es a la página correcta
    else:
        flash('Credenciales incorrectas. Inténtelo de nuevo.')
        return redirect(url_for('form'))

@app.route('/Pantalla')
def Inicio():
    if 'usuario' in session:
        return render_template('Inicio.html', usuario=session['usuario'])  # Renderiza la pantalla de Inicio
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('form'))  # Si no ha iniciado sesión, redirige a la página de login

# Ruta para la pantalla de "Ingresar Vehículo"
@app.route('/ingresar')
def IngresarVehiculo():
    return render_template('IngresarVehiculo.html')


if __name__ == '__main__':
    app.run(debug=True)
