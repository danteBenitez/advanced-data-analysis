import pandas as pd
import matplotlib.pyplot as plt
from database import Database
from services.company import CompanyDataService
from data.analysis.performance import PerformanceAnalysis


def main():
    try:
        database = Database()
        company_data = CompanyDataService(database)
        company_data.init_table()
        performance_data = company_data.get_employees_performance()

        data_frame = pd.DataFrame(performance_data)

        performance = PerformanceAnalysis(data_frame)

        performance.describe_departments()

        # Correlación
        for (column1, column2) in [("years_with_company", "performance_score"), ("salary", "performance_score")]:
            correlation = performance.correlation_between(
                column1=column1, column2=column2)
            print(f"Correlación entre {column1} y {column2}: {correlation}")

        # Visualización de datos
        # Histogramas
        plt.subplot(3, 3, (1, 3))
        performance.histograms_by_department(department="Engineering")

        plt.subplot(3, 3, (4, 6))
        performance.histograms_by_department(department="Sales")

        plt.subplot(3, 3, (7, 9))
        performance.histograms_by_department(department="Services")

        # Dispersión
        performance.disperssion_between(
            column1="years_with_company", column2="performance_score")
        performance.disperssion_between(
            column1="salary", column2="performance_score")

        plt.show()

    except Exception as err:
        print("Ocurrió un error al ejecutar el script: ", err)


if __name__ == "__main__":
    main()
