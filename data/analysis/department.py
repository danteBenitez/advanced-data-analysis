import pandas as pd


class DepartmentAnalysis:
    def __init__(self, performance_frame: pd.DataFrame):
        self.frame = performance_frame

    def get_statistics(self, column: str):
        """
            Calcula estadísticas (media, mediana y moda) a partir de los datos pasados sobre el rendimiento de los empleados.
            Toma en consideración la columna `column`
        """
        summary = pd.DataFrame()

        summary["Media"] = self.frame.groupby(["department"])[column].mean()
        summary["Mediana"] = self.frame.groupby(["department"])[
            column].median()
        summary["Desviación estándar"] = self.frame.groupby(["department"]).std()[
            column]

        return summary

    def count_employees(self):
        """
            Calcula la cantidad de empleados por departamento
        """
        employee_count = self.frame.groupby(["department"])["id"].count()
        return employee_count

    def show_statistics(self, columns: list[str]):
        """
            Muestra las estadísticas de las columnas especificadas
        """
        print("Estadísticas de rendimiento de empleados: ")
        for column in columns:
            print(f"Por {column}")
            print(self.get_statistics(column))

    def show_employees_count(self):
        """
            Muestra la cantidad de empleados por departamento
        """
        print("Cantidad de empleados por departamento")
        print(self.count_employees())

    def histogram_for(self, department: str, *, bin_count: int = 10):
        """
            Muestra un histograma con las frecuencias dadas por `frequencies_frame` y con `bin_count`
            intervalos semiabiertos
        """
        only_deparment = self.frame[self.frame["department"]
                                    == department]["performance_score"]
        hist = only_deparment.plot.hist(bins=bin_count)
        hist.set_title(f"Histograma de performance_score para {department}")
