import pyodbc

def get_connection():
    try:
        connection = pyodbc.connect(
            # AQUI VAN LOS DATOS DEL SERVIDOR (EN ESTE CASO ES UN SERVIDOR LOCAL)
            'DRIVER={SQL Server};'
            'SERVER=CHACO-LAPTOP\SQLEXPRESS;'
            'DATABASE=RentACar;'
            'Trusted_Connection=yes;'
        )
        print("Conexión exitosa a la base de datos.")
        return connection
    except Exception as e:
        print("Error: No se pudo conectar a la Base de Datos", e)
        return None
