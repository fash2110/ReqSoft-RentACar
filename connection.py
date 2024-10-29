import pyodbc

def get_connection():
    try:
        connection = pyodbc.connect(
            # AQUI VAN LOS DATOS DEL SERVIDOR (EN ESTE CASO ES UN SERVIDOR LOCAL)
            'DRIVER={SQL Server};'
            'SERVER=rentacar.cx40oo84oi0l.us-east-2.rds.amazonaws.com,1433;'
            'DATABASE=RentACar;'
            'uid=admin;pwd=9bUGOtPruE3feZP2L3tQ;',
            autocommit=True
        )
        print("Conexión exitosa a la base de datos.")
        return connection
    except Exception as e:
        print("Error: No se pudo conectar a la Base de Datos", e)
        return None