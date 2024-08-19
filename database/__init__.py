### Base de datos e inserción de datos ficticios
import MySQLdb as mysql
import os
from MySQLdb import cursors


DEFAULT_CONFIG = {
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

class Database:
    def __init__(self, options = DEFAULT_CONFIG):
        self.connection = Database.connect_to_db(options)

    Cursor = mysql.cursors.Cursor
    DictCursor = mysql.cursors.DictCursor
    Error = mysql.DatabaseError

    @staticmethod
    def connect_to_db(options: dict[str, str]) -> mysql.Connection:
        """
            Conecta a una base de datos MySQL con los paramétros especificados,
            o utiliza una serie de parámetros por defecto.

            :param Opciones de conexión
                    - "user": Usuario de la base de datos
                    - "password": Contraseña
                    - "host": Host de la base de datos (por defecto 127.0.0.1)
                    - "port": Puerto de la base de datos.
        """
        return mysql.connect(**options)
    
    def cursor(self) -> Cursor:
        """
            Retorna un cursor para la conexión actual
            Los resultados de este cursor se retornan como una tupla.
            Para un retorno en forma de diccionario, use `dict_cursor`.
        """
        return self.connection.cursor()
    
    def dict_cursor(self) -> Cursor:
        """
            Retorna un cursor para la conexión actual
            cuyos resultados se ordenan en un diccionario
        """
        return self.connection.cursor(cursors.DictCursor)

    def commit(self):
        """
            Realiza un commit de la transacción actual
        """
        self.connection.commit()
    
    def rollback(self):
        """
            Realiza un rollback de la transacción actual
        """
        self.connection.rollback()