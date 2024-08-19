import pandas as pd
import matplotlib.pyplot as plt
from database import Database
from services.company import CompanyDataService
from services.department import DepartmentService

### Análisis de datos



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
        database = Database()
        service = CompanyDataService(database)
        service.init_table()
        performance = service.get_employees_performance()
        data_frame = pd.DataFrame(performance)

        department_service = DepartmentService(data_frame)

        department_service.show_statistics(["performance_score", "salary"])
        department_service.show_employees_count()

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