-- **************************** LOGIN *********************************

-- VALIDAR EL USUARIO

CREATE PROCEDURE dbo.ValidarUsuario
    @innombre VARCHAR(64),
    @incontrasena VARCHAR(64)

AS
BEGIN
    BEGIN TRY
		
        DECLARE @contrasenatabla VARCHAR(64);

        SELECT @contrasenatabla = contrasena
        FROM dbo.Usuarios
        WHERE nombre = @innombre;

        IF @contrasenatabla IS NULL
        BEGIN
            RETURN 1;  -- NO EXISTE
        END

        IF @contrasenatabla != @incontrasena
        BEGIN
            RETURN 2;  -- CONTRASEÑA INCORRECTA
        END

        RETURN 0;

    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- *********************  GESTION VEHÍCULOS **************************

-- INSERTAR VEHÍCULO

CREATE PROCEDURE dbo.InsertarVehiculo
	@inplaca VARCHAR(6),
	@inmodelo VARCHAR(16),
	@inmarca VARCHAR(32),
	@inanno DATE,
	@incolor VARCHAR(32),
	@inidTipo INT,
	@inidCombustible INT,
	@inidTransmision INT,
	@inidEstado INT,
	@indescripcion VARCHAR(256)

AS
BEGIN
	BEGIN TRY
		
		INSERT INTO dbo.Vehiculos(
			placa,
			modelo,
			marca,
			anno,
			color,
			idTipo,
			idCombustible,
			idTransmision,
			idEstado,
			descripcion)
		VALUES(
			@inplaca,
			@inmodelo,
			@inmarca,
			@inanno,
			@incolor,
			@inidTipo,
			@inidCombustible,
			@inidTransmision,
			@inidEstado,
			@indescripcion);

	END TRY
	BEGIN CATCH
		RETURN ERROR_NUMBER();
	END CATCH
END;
GO

-- MODIFICAR VEHÍCULO

CREATE PROCEDURE dbo.ModificarVehiculo
	@inplaca VARCHAR(6),
	@inmodelo VARCHAR(16),
	@inmarca VARCHAR(32),
	@inanno DATE,
	@incolor VARCHAR(32),
	@inidTipo INT,
	@inidCombustible INT,
	@inidTransmision INT,
	@inidEstado INT,
	@indescripcion VARCHAR(256)

AS
BEGIN
	BEGIN TRY
		UPDATE dbo.Vehiculos
			SET color = @incolor,
				idTipo = @inidTipo,
				idCombustible = @inidCombustible,
				idTransmision = @inidTransmision,
				idEstado = @inidEstado,
				descripcion = @indescripcion
			WHERE placa = @inplaca;
	END TRY
	BEGIN CATCH
		RETURN ERROR_NUMBER();
	END CATCH
END;
GO

-- ELIMINAR VEHÍCULO

CREATE PROCEDURE dbo.EliminarVehiculo
	@inplaca VARCHAR(6)

AS
BEGIN
	BEGIN TRY
		DELETE FROM dbo.Vehiculos
		WHERE placa = @inplaca;
	END TRY
	BEGIN CATCH
		RETURN ERROR_NUMBER();
	END CATCH
END;
GO

-- CONSULTA VEHICULO

CREATE PROCEDURE dbo.ConsultaVehiculo
	@inplaca VARCHAR(6)

AS
BEGIN
    BEGIN TRY
        IF EXISTS (SELECT 1 FROM dbo.Vehiculos WHERE placa = @inplaca)
        BEGIN
            SELECT placa,
				modelo,
				marca,
				anno,
				color,
				idTipo,
				idCombustible,
				idTransmision,
				idEstado,
				descripcion
            FROM dbo.Vehiculos
            WHERE placa = @inplaca;
        END
        ELSE
        BEGIN
            RETURN 1;  -- NO EXISTE
        END
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- LISTA DE VEHÍCULOS

CREATE PROCEDURE dbo.ListarVehiculos

AS
BEGIN
	BEGIN TRY
		SELECT * FROM dbo.Vehiculos;
	END TRY
	BEGIN CATCH
		RETURN ERROR_NUMBER();
	END CATCH
END;
GO

-- *********************  GESTION ALQUILERES **************************

-- INSERTAR ALQUILER

CREATE PROCEDURE dbo.InsertarAlquiler
    @inidVehiculo VARCHAR(6),
    @infechaInicio DATETIME,
    @infechaFin DATETIME,
    @incliente VARCHAR(64),
    @inmonto FLOAT

AS
BEGIN
    BEGIN TRY
        INSERT INTO dbo.Alquileres(idVehiculo, fechaInicio, fechaFin, cliente, monto)
        VALUES (@inidVehiculo, @infechaInicio, @infechaFin, @incliente, @inmonto);
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- MODIFICAR ALQUILER

CREATE PROCEDURE dbo.ModificarAlquiler
    @inidalquiler INT,
    @inidVehiculo VARCHAR(6),
    @infechaInicio DATETIME,
    @infechaFin DATETIME,
    @incliente VARCHAR(64),
    @inmonto FLOAT

AS
BEGIN
    BEGIN TRY
        UPDATE dbo.Alquileres
        SET idVehiculo = @inidVehiculo,
            fechaInicio = @infechaInicio,
            fechaFin = @infechaFin,
            cliente = @incliente,
            monto = @inmonto
        WHERE id = @inidalquiler;
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- ELIMINAR ALQUILER

CREATE PROCEDURE dbo.EliminarAlquiler
    @inidalquiler INT

AS
BEGIN
    BEGIN TRY
        DELETE FROM dbo.Alquileres
        WHERE id = @inidalquiler;
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- LISTAR ALQUILERES

CREATE PROCEDURE dbo.ListarAlquileres

AS
BEGIN
    BEGIN TRY
        SELECT * FROM dbo.Alquileres;
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- CONSULTAR ALQUILER

CREATE PROCEDURE dbo.ConsultarAlquiler
    @inidalquiler INT

AS
BEGIN
    BEGIN TRY
        IF EXISTS (SELECT 1 FROM dbo.Alquileres WHERE id = @inidalquiler)
        BEGIN
            SELECT idVehiculo, fechaInicio, fechaFin, cliente, monto
            FROM dbo.Alquileres
            WHERE id = @inidalquiler;
        END
        ELSE
        BEGIN
            RETURN 1;  -- NO EXISTE
        END
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- *********************  GESTION MANTENIMIENTOS **************************

CREATE PROCEDURE dbo.InsertarMantenimiento
    @inidVehiculo VARCHAR(6),
    @infecha DATETIME,
    @inmonto FLOAT,
    @indescripcion VARCHAR(64)

AS
BEGIN
    BEGIN TRY
        INSERT INTO dbo.Mantenimientos(idVehiculo, fecha, monto, descripcion)
        VALUES (@inidVehiculo, @infecha, @inmonto, @indescripcion);
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- MODIFICAR MANTENIMIENTO

CREATE PROCEDURE dbo.ModificarMantenimiento
    @inidmantenimiento INT,
    @inidVehiculo VARCHAR(6),
    @infecha DATETIME,
    @inmonto FLOAT,
    @indescripcion VARCHAR(64)

AS
BEGIN
    BEGIN TRY
        UPDATE dbo.Mantenimientos
        SET idVehiculo = @inidVehiculo,
            fecha = @infecha,
            monto = @inmonto,
            descripcion = @indescripcion
        WHERE id = @inidmantenimiento;
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- ELIMINAR MANTENIMIENTO

CREATE PROCEDURE dbo.EliminarMantenimiento
    @inidmantenimiento INT

AS
BEGIN
    BEGIN TRY
        DELETE FROM dbo.Mantenimientos
        WHERE id = @inidmantenimiento;
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- LISTAR MANTENIMIENTOS

CREATE PROCEDURE dbo.ListarMantenimientos

AS
BEGIN
    BEGIN TRY
        SELECT * FROM dbo.Mantenimientos;
    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- CONSULTAR MANTENIMIENTO

CREATE PROCEDURE dbo.ConsultarMantenimiento
    @inidmantenimiento INT

AS
BEGIN
BEGIN TRY
        IF EXISTS (SELECT 1 FROM dbo.Mantenimientos WHERE id = @inidmantenimiento)
        BEGIN
            SELECT idVehiculo, fecha, monto, descripcion
            FROM dbo.Mantenimientos
            WHERE id = @inidmantenimiento
	END
        ELSE
        BEGIN
	        RETURN;
        END
END TRY
BEGIN CATCH
	        RETURN ERROR_NUMBER();
END CATCH
END;
GO


-- **************************** REPORTES *********************************

CREATE PROCEDURE dbo.ConsultarReportes
    @infecha DATE

AS
BEGIN
    BEGIN TRY
        -- Seleccionar mantenimientos del mes con montos negativos
        SELECT 
            'Mantenimiento' AS Descripcion, 
            (monto * -1) AS Monto,  
            fecha
        FROM dbo.Mantenimientos
        WHERE MONTH(fecha) = MONTH(@infecha) AND YEAR(fecha) = YEAR(@infecha)

        UNION ALL

        -- Seleccionar alquileres del mes con montos positivos
        SELECT 
            'Alquiler' AS Descripcion, 
            monto AS Monto,  
            fechainicio AS fecha
        FROM dbo.Alquileres
        WHERE MONTH(fechainicio) = MONTH(@infecha) AND YEAR(fechainicio) = YEAR(@infecha)

        UNION ALL

        -- Seleccionar gastos de Riteve con montos negativos
        SELECT 
            'Riteve' AS Descripcion, 
            (monto * -1) AS Monto,  
            fecha
        FROM dbo.Riteve
        WHERE MONTH(fecha) = MONTH(@infecha) AND YEAR(fecha) = YEAR(@infecha)

        ORDER BY fecha;

        -- Total de los montos (incluye tanto mantenimientos como alquileres y riteve)
        SELECT SUM(monto) AS TotalMonto
        FROM (
            SELECT monto * -1 AS monto
            FROM dbo.Mantenimientos
            WHERE MONTH(fecha) = MONTH(@infecha) AND YEAR(fecha) = YEAR(@infecha)

            UNION ALL

            SELECT monto AS monto
            FROM dbo.Alquileres
            WHERE MONTH(fechainicio) = MONTH(@infecha) AND YEAR(fechainicio) = YEAR(@infecha)

            UNION ALL

            SELECT monto * -1 AS monto
            FROM dbo.Riteve
            WHERE MONTH(fecha) = MONTH(@infecha) AND YEAR(fecha) = YEAR(@infecha)
        ) AS Reportes;

    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO

-- ****************************** CALENDARIO ******************************

CREATE PROCEDURE dbo.Calendario
    @infecha DATE

AS
BEGIN
    BEGIN TRY
        -- Seleccionar los mantenimientos del mes
        SELECT 
            fecha AS Fecha, 
            'Mantenimiento' AS Descripcion, 
            CONCAT('Mantenimiento - ', descripcion) AS Detalle
        FROM dbo.Mantenimientos
        WHERE MONTH(fecha) = MONTH(@infecha) AND YEAR(fecha) = YEAR(@infecha)

        UNION ALL

        -- Seleccionar los alquileres del mes
        SELECT 
            fechainicio AS Fecha, 
            'Alquiler' AS Descripcion, 
            CONCAT('Alquiler - ', idVehiculo, ' - Cliente') AS Detalle
        FROM dbo.Alquileres
        WHERE MONTH(fechainicio) = MONTH(@infecha) AND YEAR(fechainicio) = YEAR(@infecha)

        UNION ALL

        -- Seleccionar Riteve del mes
        SELECT 
            fecha AS Fecha, 
            'Riteve' AS Descripcion, 
            'Riteve - Revisión técnica' AS Detalle
        FROM dbo.Riteve
        WHERE MONTH(fecha) = MONTH(@infecha) AND YEAR(fecha) = YEAR(@infecha)

        ORDER BY Fecha;

    END TRY
    BEGIN CATCH
        RETURN ERROR_NUMBER();
    END CATCH
END;
GO
