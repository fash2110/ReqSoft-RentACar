from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import timedelta
from datetime import datetime
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


@app.route('/logout')
def logout():
    # Cierra la sesión eliminando la información del usuario
    session.pop('usuario', None)
    return redirect(url_for('form'))  # Redirige a la página de inicio de sesión

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

@app.route('/consulta_alquiler/<id>')
def consulta_alquileres(id):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Llamar al SP para consultar los alquileres del vehículo
        cursor.execute("EXEC ConsultarAlquiler @inplaca = ?", (id,))
        alquileres = cursor.fetchall()

        # Consulta la información del vehículo
        cursor.execute("SELECT marca, modelo, anno FROM Vehiculos WHERE placa = ?", (id,))
        vehiculo_info = cursor.fetchone()

        # Validación de datos
        if not vehiculo_info:
            flash('No se encontraron detalles para este vehículo.')
            return redirect(url_for('Inicio'))

        if not alquileres:
            flash('No hay registros de alquileres para este vehículo.')
            return redirect(url_for('detalles_vehiculo', id=id))

        return render_template('ConsultaAlquileres.html', alquileres=alquileres, vehiculo=vehiculo_info)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Inicio'))

    finally:
        connection.close()


@app.route('/vendidos')
def vendidos():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Llamar al Stored Procedure con la fecha actual
        cursor.execute("EXEC dbo.Calendario @infecha = ?", (datetime.now(),))
        calendario = cursor.fetchall()

        return render_template('vendidos.html', calendario=calendario)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Inicio'))

    finally:
        connection.close()


# Ruta para mostrar el formulario de inserción de alquiler
@app.route('/vehiculo/<id>/insertar_alquiler', methods=['GET'])
def mostrar_formulario_alquiler(id):
    return render_template('InsertarAlquiler.html', id_vehiculo=id)


# Ruta para procesar la inserción de alquiler
@app.route('/vehiculo/insertar_alquiler', methods=['POST'])
def insertar_alquiler():
    id_vehiculo = request.form['id_vehiculo']
    fecha_inicio = request.form['fecha_inicio']
    fecha_fin = request.form['fecha_fin']
    cliente = request.form['cliente']
    monto = request.form['monto']

    try:
        connection = get_connection()
        cursor = connection.cursor()

        # Ejecuta el SP para insertar el alquiler
        cursor.execute(
            "EXEC InsertarAlquiler @inidVehiculo=?, @infechaInicio=?, @infechaFin=?, @incliente=?, @inmonto=?",
            (id_vehiculo, fecha_inicio, fecha_fin, cliente, monto))

        connection.commit()
        flash("Alquiler insertado exitosamente.")
        return redirect(url_for('consulta_alquileres', id=id_vehiculo))
    except Exception as e:
        flash(str(e))
        print(str(e))
        return redirect(url_for('mostrar_formulario_alquiler', id=id_vehiculo))
    finally:
        connection.close()


@app.route('/reportes', methods=['GET'])
def reportes():
    mes = request.args.get('mes')
    try:
        connection = get_connection()
        cursor = connection.cursor()

        reportes_data = []

        if mes and mes != "":
            # Ejecutar SP para filtrar reportes por mes
            cursor.execute("EXEC FiltrarReportesPorMes ?", mes)
            reportes_data = [{'descripcion': row[0], 'monto': row[1], 'fecha': row[2]} for row in cursor.fetchall()]
        else:
            # Ejecutar SP para listar alquileres
            cursor.execute("EXEC ListarAlquileres")
            alquileres = cursor.fetchall()

            # Ejecutar SP para listar mantenimientos
            cursor.execute("EXEC ListarMantenimientos")
            mantenimientos = cursor.fetchall()

            # Ejecutar SP para listar riteve
            cursor.execute("EXEC ListarRiteve")
            riteve = cursor.fetchall()


            # Añadir datos de alquileres a la lista de reportes
            for alquiler in alquileres:
                reportes_data.append({
                    'descripcion': f'Alquiler - {alquiler[4]}',  # cliente en alquiler[4]
                    'monto': alquiler[5],  # monto en alquiler[5]
                    'fecha': alquiler[2]  # fecha en alquiler[2]
                })

            # Añadir datos de mantenimientos a la lista de reportes
            for mantenimiento in mantenimientos:
                reportes_data.append({
                    'descripcion': f'Mantenimiento - {mantenimiento[1]}',  # Suponiendo que la columna descripción es la tercera
                    'monto': mantenimiento[3],  # Suponiendo que la columna costo es la cuarta
                    'fecha': mantenimiento[2]  # fecha en mantenimiento[2]
                })

            # Añadir datos de riteve a la lista de reportes
            for rev in riteve:
                reportes_data.append({
                    'descripcion': f'Riteve - {rev[1]}',  # descripción en rev[4]
                    'monto': rev[3],  # monto en rev[3]
                    'fecha': rev[2]  # fecha en rev[2]
                })

        # Convertir las fechas a objetos datetime antes de ordenar
        for reporte in reportes_data:
            if isinstance(reporte['fecha'], str):
                reporte['fecha'] = datetime.strptime(reporte['fecha'], '%Y-%m-%d')

        # Ordenar la lista de reportes por fecha
        reportes_data.sort(key=lambda x: x['fecha'])

        return render_template('Reportes.html', reportes=reportes_data, mes=mes)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Inicio'))
    finally:
        connection.close()

@app.route('/vehiculo/<id>')
def vehiculo(id):
    try:
        # Conexión con la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        # Consulta de detalles del vehículo
        cursor.execute("{CALL dbo.ConsultaVehiculo(?)}", (id,))
        vehiculo = cursor.fetchone()

        # Validación de existencia del vehículo
        if not vehiculo:
            flash('No se encontraron detalles para este vehículo.')
            return redirect(url_for('Inicio'))

        # Consulta de alquileres del vehículo
        cursor.execute("EXEC ConsultarAlquiler @inplaca = ?", (id,))
        alquileres = cursor.fetchall()

        # Consulta de mantenimientos del vehículo (pendiente de implementar)
        mantenimientos = []  # Puedes modificar esto cuando la funcionalidad de mantenimientos esté lista

        return render_template('Vehiculo.html', vehiculo=vehiculo, alquileres=alquileres, mantenimientos=mantenimientos)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Inicio'))
    finally:
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)
