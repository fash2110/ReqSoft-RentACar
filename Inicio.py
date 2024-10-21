from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Datos simulados de vehículos
vehicles = [
    {"id": 1, "brand": "Toyota", "model": "Camry 2020", "status": "Disponible"},
    {"id": 2, "brand": "Toyota", "model": "Corolla 2006", "status": "Disponible"},
    {"id": 3, "brand": "Hyundai", "model": "Grand i10 Sedan 2020", "status": "Disponible"},
    {"id": 4, "brand": "Toyota", "model": "Corolla 2012", "status": "Disponible"},
    {"id": 5, "brand": "Kia", "model": "Soul 2008", "status": "Mantenimiento"},
    {"id": 6, "brand": "Honda", "model": "Civic 2005", "status": "Disponible"},
    {"id": 7, "brand": "Toyota", "model": "4Runner 2004", "status": "Alquiler"},
    {"id": 8, "brand": "Suzuki", "model": "Swift 2016", "status": "Disponible"}
]

@app.route('/')
def Inicio():
    return render_template('Inicio.html', vehicles=vehicles)

# Ruta para la pantalla de "Ingresar Vehículo"
@app.route('/ingresar')
def IngresarVehiculo():
    return render_template('IngresarVehiculo.html')

# Ruta para la pantalla de "reportes"
@app.route('/reportes')
def reportes():
    return render_template('reportes.html')

@app.route('/Pantalla', methods=['POST'])
def PantallaPrincipal():
    data = request.json
    vehicle_id = data.get('vehicle_id')
    new_status = data.get('new_status')
    
    # Actualizamos el estado del vehículo
    for vehicle in vehicles:
        if vehicle['id'] == vehicle_id:
            vehicle['status'] = new_status
            break

    return jsonify({'success': True, 'vehicles': vehicles})

if __name__ == '__main__':
    app.run(debug=True)

