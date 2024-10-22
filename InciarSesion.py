from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta
from connection import get_connection
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave más segura en producción


@app.route('/')
def form():
    return render_template('IniciarSesion.html')

@app.route('/login', methods=['POST'])
def login():

    # DATOS DE LA APLICACION
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']
    recordarme = request.form.get('recordarme')

    try:
        # CONEXION BD: RentACar
        connection = get_connection()

        cursor = connection.cursor()
        cursor.execute("SELECT contrasena FROM Usuarios WHERE nombre = ?", (usuario,))
        result = cursor.fetchone()

        # VERIFICACION DE LOGIN
        if result and result[0] == contrasena:
            session['usuario'] = usuario
            # RECORDAR USUARIO
            if recordarme:
                session.permanent = True
                app.permanent_session_lifetime = timedelta(days=7)
            else:
                session.permanent = False
            # PANTALLA PRINCIPAL
            return redirect(url_for('Inicio'))
        else:
            flash('Credenciales incorrectas. Inténtelo de nuevo.')
            return redirect(url_for('form'))

    except Exception as e:
        flash(str(e))
        return redirect(url_for('form'))
    finally:
        connection.close()

# Ruta para la pantalla principal (Inicio)
@app.route('/Pantalla')
def Inicio():
    if 'usuario' in session:
        try:
            # CONEXION A BD RENTACAR
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("EXEC dbo.ListarVehiculos")  # STORED PROCEDURE
            vehiculos = cursor.fetchall()

            return render_template('Inicio.html', vehiculos=vehiculos)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('form'))
        finally:
            connection.close()
    else:
        flash('Por favor, inicie sesión primero.')
        return redirect(url_for('form'))

# RUTAS DE INICIO
@app.route('/ingresar')
def IngresarVehiculo():
    return render_template('Inicio.html', usuario=session['usuario'])


@app.route('/detalles/<id>')
def detalles_vehiculo(id):
    try:

        #CONEXION CON BASE DE DATOS
        connection = get_connection()
        cursor = connection.cursor()

        # LLAMADO A STORED PROCEDURE
        cursor.execute("{CALL dbo.ConsultaVehiculo(?)}", (id,))
        vehiculo = cursor.fetchone()

        # VALIDACIÓN DE EXISTENCIA DE VEHÍCULO
        if vehiculo:
            return render_template('Vehiculosdetalles.html', vehiculo=vehiculo)
        else:
            flash('No se encontraron detalles para este vehículo.')
            return redirect(url_for('Inicio'))

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Inicio'))
    finally:
        connection.close()

@app.route('/modificar/<id>', methods=['GET', 'POST'])
def modificar_vehiculo(id):
    if request.method == 'POST':

        # DATOS DE LA APLICACION
        color = request.form['color']
        idTipo = request.form['idTipo']
        idCombustible = request.form['idCombustible']
        idTransmision = request.form['idTransmision']
        idEstado = request.form['idEstado']
        descripcion = request.form['descripcion']

        try:

            # CONEXION CON BASE DE DATOS
            connection = get_connection()
            cursor = connection.cursor()

            # LLAMADO AL STORED PROCEDURE
            cursor.execute("""
                EXEC dbo.ModificarVehiculo
                    @inplaca=?,
                    @inmodelo=?,
                    @inmarca=?,
                    @inanno=?,
                    @incolor=?,
                    @inidTipo=?,
                    @inidCombustible=?,
                    @inidTransmision=?,
                    @inidEstado=?,
                    @indescripcion=?
            """, (id, None, None, None, color, idTipo, idCombustible, idTransmision, idEstado, descripcion))

            connection.commit()

            return redirect(url_for('detalles_vehiculo', id=id))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('detalles_vehiculo', id=id))
        finally:
            connection.close()
    else:
        try:

            # CONEXION CON BASE DE DATOS
            connection = get_connection()
            cursor = connection.cursor()
            cursor.execute("EXEC dbo.ConsultaVehiculo ?", (id,))
            vehiculo = cursor.fetchone()

            if vehiculo:
                return render_template('ModificarVehiculo.html', vehiculo=vehiculo)
            else:
                flash('No se encontraron detalles para este vehículo.')
                return redirect(url_for('Inicio'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('Inicio'))
        finally:
            connection.close()


@app.route('/vehiculos/<id>/eliminar', methods=['POST'])
def eliminar_vehiculo(id):

    try:

        # CONEXION A LA BASE DE DATOS
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("EXEC EliminarVehiculo @inplaca = ?", (id,))
        connection.commit()

    except Exception as e:
        flash(str(e))
    finally:
        connection.close()

    return redirect(url_for('Inicio'))


@app.route('/reportes')
def reportes():
    return render_template('reportes.html')


if __name__ == '__main__':
    app.run(debug=True)
