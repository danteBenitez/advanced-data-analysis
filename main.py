import MySQLdb as mysql
from MySQLdb import cursors
import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

### Base de datos e inserción de datos ficticios

MOCK_DATA_PATH = "MOCK_DATA.csv"

DEFAULT_CONFIG = {
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "root"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", "3306")),
}

def connect_to_db(options: dict[str, str] = DEFAULT_CONFIG) -> mysql.Connection:
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

class CompanyDataService:
    def __init__(self, conn: mysql.Connection):
        self.connection = conn

    def init_table(self):
        """
            Inicializa una base de datos llamada `CompanyData`.
            Crea la base de datos, y una tabla `EmployeePerformance`, la cual
            pobla con datos ficticios
        """
        try:
            cursor: cursors.Cursor = self.connection.cursor()
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
        except mysql.DatabaseError as err:
            self.connection.rollback()
            print("Ocurrió un error al inicializar tabla CompanyData: ", err) 
        finally:
            cursor.close()
    
    def seed_table(cursor: cursors.Cursor):
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
    
    def get_employees_performance(self) -> cursors.DictCursor:
        """
            Retorna un cursor sobre todos los registros de la tabla EmployeePerformance.
            
            :returns Un cursor de tipo diccionario sobre los datos obtenidos.
            :rtype cursors.DictCursor
        """
        try:
            cursor: cursors.DictCursor = self.connection.cursor(mysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM EmployeePerformance")
            return cursor
        except mysql.Error as err:
            cursor.close()
            print("No se pudo realizar la consulta: ", err)


### Análisis de datos

def calculate_statistics_by_deparment(performace_frame: pd.DataFrame, *, column: str):
    """
        Calcula estadísticas (media, mediana y moda) a partir de los datos pasados sobre el rendimiento de los empleados.
        Toma en consideración la columna `column`
    """
    summary = pd.DataFrame()

    summary["Media"] = performace_frame.groupby(["department"])[column].mean()
    summary["Mediana"] = performace_frame.groupby(["department"])[column].median()
    summary["Desviación estándar"] = performace_frame.groupby(["department"]).std()[column]

    return summary
    # Correlación entre salary y performance_score.

def employees_by_department(performance_frame: pd.DataFrame):
    """
        Calcula la cantidad de empleados por departamento
    """
    employee_count = performance_frame.groupby(["department"])["id"].count()
    return employee_count

def correlation_between(performance_frame: pd.DataFrame, *, column1: str, column2: str):
    """
        Calcula la correlación entre las dos columnas especificadas según los datos de `performance_frame`
    """
    return performance_frame.corr(numeric_only=True)[column1][column2]

### Visualización de datos
def show_histograms_for_deparment(plot: plt.plot, performance_frame: pd.DataFrame, bin_count: int, department: str):
    """
        Muestra un histograma con las frecuencias dadas por `frequencies_frame` y con `bin_count`
        intervalos semiabiertos
    """
    only_deparment = performance_frame[performance_frame["department"] == department]["performance_score"]
    hist = only_deparment.plot.hist(bins=bin_count)
    hist.set_title(f"Histograma de performance_score para {department}")

def show_disperssion_between(performance_frame: pd.DataFrame, *, column1: str, column2: str):
    """
        Muestra un gráfico de dispersión entre los datos de ambas columnas 
    """
    performance_frame.plot.scatter(x=column1, y=column2)


def main():
    try:
        connection = connect_to_db()
        service = CompanyDataService(connection)
        service.init_table()
        performance = service.get_employees_performance()
        data_frame = pd.DataFrame(performance)

        # Media, mediana y desviación estándar del performance_score.
        by_performance_score = calculate_statistics_by_deparment(data_frame, column="performance_score")
        print("Por performance_score")
        print(by_performance_score)

        # Media, mediana y desviación estándar del salary.
        by_salary = calculate_statistics_by_deparment(data_frame, column="salary")
        print("Por salary")
        print(by_salary)

        # Número total de empleados por departamento.
        employees_count = employees_by_department(data_frame)
        print("Empleados por departamento")
        print(employees_count)

        # Correlación 
        correlation_years_score = correlation_between(data_frame, column1="years_with_company", column2="performance_score")
        print("Correlación entre years_with_company y performance_score")
        print(correlation_years_score)

        correlation_salary_score = correlation_between(data_frame, column1="salary", column2="performance_score")
        print("Correlación entre salary y performance_score")
        print(correlation_salary_score)

        # Visualización de datos
        # Histogramas
        subplot1 = plt.subplot(3, 3, (1, 3))
        show_histograms_for_deparment(subplot1, data_frame, department="Engineering", bin_count=10)

        subplot2 = plt.subplot(3, 3, (4, 6))
        show_histograms_for_deparment(subplot2, data_frame, department="Sales", bin_count=10)

        subplot3 = plt.subplot(3, 3, (7, 9))
        show_histograms_for_deparment(subplot3, data_frame, department="Services", bin_count=10)

        # Dispersión
        show_disperssion_between(data_frame, column1="years_with_company", column2="performance_score")
        show_disperssion_between(data_frame, column1="salary", column2="performance_score")

        plt.show()
    except Exception as err:
        print("Ocurrió un error al ejecutar el script: ", err)

if __name__ == "__main__":
    main()