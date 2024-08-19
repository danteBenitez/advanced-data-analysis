from database import Database
import csv

MOCK_DATA_PATH = "MOCK_DATA.csv"

class CompanyDataService:
    """
        Servicio que interactúa con la base de datos `CompanyData`. 
        Provee métodos para inicializar la base de datos, poblarla con datos ficticios,
        y obtener información de la tabla `EmployeePerformance`.
    """

    def __init__(self, conn: Database):
        self.connection = conn

    def init_table(self):
        """
            Inicializa una base de datos llamada `CompanyData`.
            Crea la base de datos, y una tabla `EmployeePerformance`, la cual
            pobla con datos ficticios
        """
        try:
            cursor: Database.Cursor = self.connection.cursor()
            cursor.execute("""
                DROP DATABASE IF EXISTS CompanyData
            """)
            cursor.execute("""
                CREATE DATABASE CompanyData
            """) 
            cursor.execute("""
                USE CompanyData
            """)
            cursor.execute("""
                CREATE TABLE EmployeePerformance (
                    id int AUTO_INCREMENT PRIMARY KEY,
                    employee_id int,
                    department text,
                    performance_score float,
                    years_with_company int,
                    salary float 
                )
            """)
            CompanyDataService.seed_table(cursor)
            self.connection.commit()
        except Database.Error as err:
            self.connection.rollback()
            print("Ocurrió un error al inicializar tabla CompanyData: ", err) 
        finally:
            cursor.close()
    
    def seed_table(cursor: Database.Cursor):
        """
            Inicializa la tabla EmployeePerformance con datos ficticios.
        """
        with open(MOCK_DATA_PATH) as file:
            reader = csv.reader(file)
            next(reader)
            # Mapeamos las filas que retorna el reader (en forma de lista)
            # a tuplas

            # Nótese que `map` retorna un iterable, por lo que los elementos
            # se calculan conforme se van necesitando. La lista *no* se carga
            # completamente en memoria.
            mapped = map(lambda lst: (lst[0], lst[1], lst[2], lst[3], lst[4], lst[5]), reader)

            # `executemany` tiene mejor rendimiento que su contraparte singular al insertar
            # múltiples registros.
            cursor.executemany("""
                INSERT INTO EmployeePerformance (
                    id, employee_id, department, performance_score,
                    years_with_company, salary
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, mapped)
    
    def get_employees_performance(self) -> Database.DictCursor:
        """
            Retorna un cursor sobre todos los registros de la tabla EmployeePerformance.
            
            :returns Un cursor de tipo diccionario sobre los datos obtenidos.
            :rtype cursors.DictCursor
        """
        try:
            cursor: Database.DictCursor = self.connection.dict_cursor()
            cursor.execute("SELECT * FROM EmployeePerformance")
            return cursor
        except Database.Error as err:
            cursor.close()
            print("No se pudo realizar la consulta: ", err)