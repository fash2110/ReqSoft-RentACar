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
        if result and result[0] == True or contrasena:
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
@app.route('/ingresar_vehiculo', methods=['GET', 'POST'])
def ingresar_vehiculo():
    try:
        # Conexión con la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        # Cargar datos desde las tablas de referencia
        cursor.execute("SELECT id, nombre FROM Tipos")
        tipos = cursor.fetchall()

        cursor.execute("SELECT id, nombre FROM Combustibles")
        combustibles = cursor.fetchall()

        cursor.execute("SELECT id, nombre FROM Transmision")
        transmisiones = cursor.fetchall()

        cursor.execute("SELECT id, nombre FROM Estados")
        estados = cursor.fetchall()

        if request.method == 'POST':
            placa = request.form['placa']
            modelo = request.form['modelo']
            marca = request.form['marca']
            anno = request.form['anno']
            color = request.form['color']
            id_tipo = request.form['tipo']
            id_combustible = request.form['combustible']
            id_transmision = request.form['transmision']
            id_estado = request.form['estado']
            descripcion = request.form['descripcion']

            # Insertar el vehículo
            cursor.execute("""
                INSERT INTO Vehiculos (placa, modelo, marca, anno, color, idTipo, idCombustible, idTransmision, idEstado, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (placa, modelo, marca, anno, color, id_tipo, id_combustible, id_transmision, id_estado, descripcion))
            connection.commit()

            flash('Vehículo ingresado con éxito.')
            return redirect(url_for('Inicio'))

        return render_template('IngresarVehiculo.html', tipos=tipos, combustibles=combustibles, transmisiones=transmisiones, estados=estados)

    except Exception as e:
        flash(f"Error al cargar los datos: {str(e)}")
        return redirect(url_for('Inicio'))
    finally:
        if 'connection' in locals():
            connection.close()


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
            return render_template('VehiculosDetalles.html', vehiculo=vehiculo)
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

            print('SE CONECTÓ AL ORIGINAL)')

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

            return redirect(url_for('vehiculo', id=id))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('vehiculo', id=id))
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

        print(id)

        # CONEXION A LA BASE DE DATOS
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("EXEC EliminarVehiculo @inplaca = ?", (id,))
        connection.commit()

    except Exception as e:
        flash(str(e))
        print(str(e))

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
        resultados = [
            {
                'Fecha': row.Fecha,
                'FechaFin': row.FechaFin,
                'Descripcion': row.Descripcion,
                'Detalle': row.Detalle
            } for row in calendario
        ]

        return render_template('vendidos.html', calendario=resultados)

    except Exception as e:
        flash(str(e))
        return redirect(url_for('Inicio'))

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

        # Consulta de mantenimientos del vehículo
        
        cursor.execute("EXEC ListarMantenimientos")
        mantenimientos = cursor.fetchall()

        # Filtrar mantenimientos relacionados al vehículo especificado por la placa
        mantenimientos = [mantenimiento for mantenimiento in mantenimientos if mantenimiento[1] == id]

        return render_template('Vehiculo.html', vehiculo=vehiculo, alquileres=alquileres, mantenimientos=mantenimientos)

    except Exception as e:
        print(str(e))
        flash(str(e))
        return redirect(url_for('Inicio'))
    finally:
        connection.close()


@app.route('/vehiculo/<id>/insertar_alquiler', methods=['GET'])
def mostrar_formulario_alquiler(id):
    # Renderizar el formulario de inserción de alquiler, pasando la placa del vehículo
    return render_template('InsertarAlquiler.html', vehiculo={'placa': id})

@app.route('/vehiculo/insertar_alquiler', methods=['POST'])
def insertar_alquiler():
    id_vehiculo = request.form['placa']
    fecha_inicio_str = request.form['fechaInicio']
    fecha_fin_str = request.form['fechaFin']
    cliente = request.form['cliente']
    monto = request.form['monto']

    try:
        # Convierte las fechas a objetos datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%dT%H:%M')
        fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%dT%H:%M')

        # Validación: La fecha de inicio debe ser antes que la fecha de fin
        if fecha_inicio >= fecha_fin:
            flash("La fecha de inicio debe ser anterior a la fecha de fin.")
            return redirect(url_for('mostrar_formulario_alquiler', id=id_vehiculo))

        connection = get_connection()
        cursor = connection.cursor()

        # Ejecuta el SP para insertar el alquiler
        cursor.execute(
            "EXEC InsertarAlquiler @inidVehiculo=?, @infechaInicio=?, @infechaFin=?, @incliente=?, @inmonto=?",
            (id_vehiculo, fecha_inicio, fecha_fin, cliente, monto))

        connection.commit()
        flash("Alquiler insertado exitosamente.")
        return redirect(url_for('vehiculo', id=id_vehiculo))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('mostrar_formulario_alquiler', id=id_vehiculo))
    finally:
        connection.close()


@app.route('/vehiculo/modificar_alquiler/<alquiler_id>', methods=['GET', 'POST'])
def modificar_alquiler(alquiler_id):
    try:
        # Conexión con la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        if request.method == 'POST':
            # Obtener los datos del formulario
            placa = request.form['placa']
            fecha_inicio_str = request.form['fechaInicio']
            fecha_fin_str = request.form['fechaFin']
            cliente = request.form['cliente']
            monto = request.form['monto']

            try:
                # Convertir las fechas de string a datetime en un formato compatible con SQL Server
                fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%dT%H:%M")
                fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%dT%H:%M")
            except ValueError as ve:
                flash(f"Formato de fecha inválido: {str(ve)}")
                return redirect(url_for('vehiculo', id=placa))

            # Ejecutar la consulta de modificación usando SQL incrustado
            cursor.execute("""
                UPDATE Alquileres
                SET idVehiculo = ?, fechaInicio = ?, fechaFin = ?, cliente = ?, monto = ?
                WHERE fechaInicio = ? AND idVehiculo = ?
            """, (placa, fecha_inicio, fecha_fin, cliente, monto, alquiler_id, placa))
            connection.commit()

            flash('El alquiler ha sido modificado con éxito.')
            return redirect(url_for('vehiculo', id=placa))

        cursor.execute("SELECT * FROM Alquileres WHERE fechaInicio = ?", (alquiler_id,))
        alquiler = cursor.fetchone()

        if not alquiler:
            flash('No se encontró el alquiler.')
            return redirect(url_for('vehiculo', id=session.get('vehiculo_id')))

        return render_template('ModificarAlquiler.html', alquiler=alquiler)

    except Exception as e:
        flash(f"Error al modificar el alquiler: {str(e)}")
        return redirect(url_for('vehiculo', id=session.get('vehiculo_id')))
    finally:
        if 'connection' in locals() and connection:
            connection.close()



# Ruta para mostrar el formulario de inserción de mantenimiento
@app.route('/vehiculo/<id>/insertar_mantenimiento', methods=['GET'])
def mostrar_formulario_mantenimiento(id):
    # Renderizar el formulario de inserción de mantenimiento, pasando la placa del vehículo
    return render_template('InsertarMantenimiento.html', vehiculo={'placa': id})

# Ruta para procesar la inserción de mantenimiento
@app.route('/vehiculo/insertar_mantenimiento', methods=['POST'])
def insertar_mantenimiento():
    id_vehiculo = request.form['placa']
    fecha = request.form['fecha']
    monto = request.form['monto']
    descripcion = request.form['descripcion']

    try:
        # Convierte las fechas a objetos datetime
        fecha = datetime.strptime(fecha, '%Y-%m-%dT%H:%M')

        connection = get_connection()
        cursor = connection.cursor()

        # Ejecuta el SP para insertar el mantenimiento
        cursor.execute(
            "EXEC InsertarMantenimiento @inidVehiculo=?, @infecha=?, @inmonto=?, @indescripcion=?",
            (id_vehiculo, fecha, monto, descripcion))

        connection.commit()
        flash("Mantenimiento insertado exitosamente.")
        return redirect(url_for('vehiculo', id=id_vehiculo))
    except Exception as e:
        flash(str(e))
        return redirect(url_for('mostrar_formulario_mantenimiento', id=id_vehiculo))
    finally:
        connection.close()

@app.route('/vehiculo/eliminar_mantenimiento', methods=['POST'])
def eliminar_mantenimiento():
    id_mantenimiento = request.form['id_mantenimiento']

    try:
        # Conexión con la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        # Ejecuta el SP para eliminar el mantenimiento
        cursor.execute("EXEC EliminarMantenimiento @inidmantenimiento=?", (id_mantenimiento,))
        connection.commit()

        flash("Mantenimiento eliminado exitosamente.")
    except Exception as e:
        flash(str(e))
    finally:
        connection.close()

    # Redirigir de nuevo a la vista del vehículo actual
    return redirect(url_for('vehiculo', id=session.get('vehiculo_id')))

@app.route('/vehiculo/modificar_mantenimiento/<int:id>', methods=['GET', 'POST'])
def modificar_mantenimiento(id):
    if request.method == 'POST':
        # Datos del formulario
        fecha_str = request.form['fecha']
        monto = request.form['monto']
        descripcion = request.form['descripcion']
        placa = request.form['placa']

        try:
            # Convertir la fecha a un objeto datetime
            fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M')

            # Conexión a la base de datos
            connection = get_connection()
            cursor = connection.cursor()

            # Ejecutar el SP para modificar el mantenimiento
            cursor.execute(
                "EXEC ModificarMantenimiento @inidmantenimiento=?, @inidVehiculo=?, @infecha=?, @inmonto=?, @indescripcion=?",
                (id, placa, fecha, monto, descripcion)
            )
            connection.commit()

            flash("Mantenimiento modificado exitosamente.")
            return redirect(url_for('vehiculo', id=placa))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('modificar_mantenimiento', id=id))
        finally:
            connection.close()
    else:
        try:
            # Conexión a la base de datos
            connection = get_connection()
            cursor = connection.cursor()

            # Consultar el mantenimiento por ID
            cursor.execute("SELECT * FROM Mantenimientos WHERE id = ?", (id,))
            mantenimiento = cursor.fetchone()

            if not mantenimiento:
                flash('No se encontraron detalles para este mantenimiento.')
                return redirect(url_for('Inicio'))

            return render_template('ModificarMantenimiento.html', mantenimiento=mantenimiento)
        except Exception as e:
            flash(str(e))
            return redirect(url_for('Inicio'))
        finally:
            connection.close()


@app.route('/vehiculo/eliminar_alquiler', methods=['POST'])
def eliminar_alquiler():
    fecha_inicio = request.form['id_alquiler']

    try:
        # Conexión con la base de datos
        connection = get_connection()
        cursor = connection.cursor()

        # Ejecuta la consulta para eliminar el alquiler usando la fecha de inicio como identificador
        cursor.execute("DELETE FROM Alquileres WHERE fechaInicio = ?", (fecha_inicio,))
        connection.commit()

        flash('El alquiler ha sido eliminado con éxito.')

        # Redireccionar de vuelta a la pantalla del vehículo
        return redirect(url_for('vehiculo', id=session.get('vehiculo_id')))
    except Exception as e:
        flash(f"Error al eliminar el alquiler: {str(e)}")
        return redirect(url_for('vehiculo', id=session.get('vehiculo_id')))
    finally:
        if 'connection' in locals() and connection:
            connection.close()

@app.route('/modificar/<id>', methods=['GET', 'POST'])
def modificar_vehiculo_inicio(id):
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

            print('SE COMECTÓ A AL DE INICIO')

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

            return redirect(url_for('Inicio'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('Inicio'))
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
                return redirect(url_for('Inicio'))
            else:
                flash('No se encontraron detalles para este vehículo.')
                return redirect(url_for('Inicio'))
        except Exception as e:
            flash(str(e))
            return redirect(url_for('Inicio'))
        finally:
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
