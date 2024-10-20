from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def form():
    return render_template('IniciarSesion.html')

@app.route('/login', methods=['POST'])
def login():
    # Obtener los datos del formulario
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    recordarme = request.form.get('recordarme')

    # Aquí puedes agregar la lógica de verificación de usuario
    # En este ejemplo, simplemente imprimo los datos en consola
    print(f"Usuario: {usuario}")
    print(f"Contraseña: {contrasena}")
    print(f"Recordarme: {recordarme}")

    # Aquí puedes agregar redireccionamiento después del login
    # En este ejemplo, redirigimos de vuelta a la página de inicio
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
