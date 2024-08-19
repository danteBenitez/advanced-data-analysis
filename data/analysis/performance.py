from data.analysis.department import DepartmentAnalysis
import pandas as pd


class PerformanceAnalysis:
    @staticmethod
    def attributes():
        """
            Atributos válidos para un registro de rendimiento de empleados
        """
        return ["id", "performance_score", "department", "years_with_company", "salary"]

    def __init__(self, frame: pd.DataFrame):
        self.frame = frame
        self.department_service = DepartmentAnalysis(frame)

    def describe_departments(self):
        """
            Muestra mediciones estadísticas de los empleados por departamento
            así como la cantidad de empleados por departamento
        """
        self.department_service.show_statistics(
            columns=["performance_score", "salary"])
        self.department_service.show_employees_count()

    def correlation_between(self, column1: str, column2: str):
        """
            Calcula la correlación entre las dos columnas especificadas según los datos de 
            rendimiento de empleados
        """
        attrs = PerformanceAnalysis.attributes()
        if column1 not in attrs or column2 not in attrs:
            raise ValueError("Las columnas especificadas no son válidas")

        return self.frame.corr(numeric_only=True)[column1][column2]

    def disperssion_between(self, *, column1: str, column2: str):
        """
            Muestra un gráfico de dispersión entre los datos de ambas columnas 
        """
        attrs = PerformanceAnalysis.attributes()
        if column1 not in attrs or column2 not in attrs:
            raise ValueError("Las columnas especificadas no son válidas")
        self.frame.plot.scatter(x=column1, y=column2)

    def histograms_by_department(self, bin_count: int = 10, *, department: str):
        """
            Muestra un histograma con las frecuencias de `performance_score` para un departamento
            específico. Divide el histograma en `bin_count` intervalos semiabiertos.
        """
        return self.department_service.histogram_for(department, bin_count=bin_count)
