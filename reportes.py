from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Ruta para mostrar el formulario HTML
@app.route('/')
def form():
    return render_template('reportes.html')

# Ruta para la pantalla de "Pantalla"
@app.route('/Pantalla')
def Inicio():
    return render_template('Inicio.html')

# Ruta principal para mostrar los reportes
@app.route('/reportes')
def reportes():
    # Generar los meses y años desde 2015 hasta 2024
    current_year = datetime.now().year
    years = list(range(2015, current_year + 1))
    
    # Generar una lista con todos los meses y años
    meses = []
    for year in reversed(years):
        for month in range(1, 13):
            mes_str = datetime(year, month, 1).strftime('%B %Y')
            mes_value = f'{year}-{month:02d}'
            meses.append((mes_value, mes_str.capitalize()))

    # Renderizar el template HTML con los meses
    return render_template('reportes.html', meses=meses)

if __name__ == '__main__':
    app.run(debug=True)
