from flask import Flask, request, render_template

app = Flask(__name__)

# Ruta para mostrar el formulario HTML
@app.route('/')
def form():
    return render_template('IngresarVehiculo.html')  # Asegúrate de que el archivo HTML se llame 'formulario.html'

# Ruta para procesar los datos del formulario
@app.route('/ingresar', methods=['POST'])
def ingresar_vehiculo():
    marca = request.form['marca']
    modelo = request.form['modelo']
    anio = request.form['anio']
    placa = request.form['placa']
    color = request.form['color']
    kilometraje = request.form['kilometraje']
    pasajeros = request.form['pasajeros']
    transmision = request.form['transmision']
    combustible = request.form['combustible']
    detalles = request.form['detalles']
    
    # Aquí puedes guardar los datos en una base de datos o archivo
    # En este caso los imprimiremos en la consola para verificarlos
    print(f'Vehículo ingresado: {marca} {modelo}, Año: {anio}, Placa: {placa}, Color: {color}, Kilometraje: {kilometraje}, Pasajeros: {pasajeros}, Transmisión: {transmision}, Combustible: {combustible}, Detalles: {detalles}')
    
    # Mostrar una respuesta en el navegador
    return f'Vehículo {marca} {modelo} ingresado exitosamente'

if __name__ == '__main__':
    app.run(debug=True)
