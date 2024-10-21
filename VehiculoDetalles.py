from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de base de datos para un vehículo
detalles_vehiculos = {
    'modelo': 'Toyota Camry',
    'anio': '2020',
    'tipo': 'Sedan',
    'detalles': {
        'placa': 'AAA-111',
        'ultima_revision': '01/01/2001',
        'transmision': 'Automático/Dual',
        'combustible': 'Gasolina',
        'capacidad_tanque': '24 Litros',
        'cilindrada': '2500CC',
        'exterior': 'Gris',
        'interior': 'Café',
        'pasajeros': '5',
        'puertas': '5'
    },
    'estado': 'Disponible'
}

@app.route('/')
def index():
    return redirect(url_for('VehiculosDetalles'))

@app.route('/detalles', methods=['GET', 'POST'])
def VehiculosDetalles():
    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'save':
            # Actualizar los datos del vehículo con lo que se envía en el formulario
            detalles_vehiculos['modelo'] = request.form.get('modelo', detalles_vehiculos['modelo'])
            detalles_vehiculos['anio'] = request.form.get('anio', detalles_vehiculos['anio'])
            detalles_vehiculos['tipo'] = request.form.get('tipo', detalles_vehiculos['tipo'])
            detalles_vehiculos['detalles']['placa'] = request.form.get('placa', detalles_vehiculos['detalles']['placa'])
            detalles_vehiculos['detalles']['ultima_revision'] = request.form.get('ultima_revision', detalles_vehiculos['detalles']['ultima_revision'])
            detalles_vehiculos['detalles']['transmision'] = request.form.get('transmision', detalles_vehiculos['detalles']['transmision'])
            detalles_vehiculos['detalles']['combustible'] = request.form.get('combustible', detalles_vehiculos['detalles']['combustible'])
            detalles_vehiculos['detalles']['capacidad_tanque'] = request.form.get('capacidad_tanque', detalles_vehiculos['detalles']['capacidad_tanque'])
            detalles_vehiculos['detalles']['cilindrada'] = request.form.get('cilindrada', detalles_vehiculos['detalles']['cilindrada'])
            detalles_vehiculos['detalles']['exterior'] = request.form.get('exterior', detalles_vehiculos['detalles']['exterior'])
            detalles_vehiculos['detalles']['interior'] = request.form.get('interior', detalles_vehiculos['detalles']['interior'])
            detalles_vehiculos['detalles']['pasajeros'] = request.form.get('pasajeros', detalles_vehiculos['detalles']['pasajeros'])
            detalles_vehiculos['detalles']['puertas'] = request.form.get('puertas', detalles_vehiculos['detalles']['puertas'])

        elif action == 'delete':
            # Acción para eliminar el vehículo, en este caso solo reseteamos los datos simulados
            global vehicle_data
            vehicle_data = {}

        return redirect(url_for('VehiculosDetalles'))

    return render_template('VehiculosDetalles.html', vehicle=detalles_vehiculos)

if __name__ == '__main__':
    app.run(debug=True)
