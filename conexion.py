import pyodbc
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Conexion:
    def __init__(self):
        direccion_servidor = self.config['BaseSQL']['server']
        nombre_bd = self.config['BaseSQL']['database']
        nombre_usuario = self.config['BaseSQL']['user']
        password = self.config['BaseSQL']['password']
        try:
            conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
                                    direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
            # OK! conexión exitosa
        except Exception as e:
            # Atrapar error
            print("Ocurrió un error al conectar a SQL Server: ", e)
    