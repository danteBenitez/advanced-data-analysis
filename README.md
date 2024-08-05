# Repaso de librerías de Python: Interacción con base de datos, análisis y visualización de datos

## Descripción

El presente proyecto realiza tareas de análisis de datos con un conjunto ficticio de datos sobre el rendimiento de empleados en una empresa. Concretamente:
    - Interactúa con un servidor de base de datos MySQL para:
        - Crear una base de datos CompanyData.
        - Crear una tabla de EmployeePerformance.
        - Insertar 1.000 registros de rendimiento de empleados ficticios, en la tabla, obtenidos de [Mockaroo](https://www.mockaroo.com/).
    - Realizar análisis de datos, por ejemplo, al:
        - Calcular datos estadísticas de relevancia como la media, la mediana y la desviación estándar.
        - Calcular la cantidad de empleados agrupados por departamento.
    - Visualizar los datos, mediante:
        - Un histograma del rendimiento de los empleados por departamento.
        - Dos gráficos de dispersión entre datos de la tabla.

## Instrucciones

- Primero, cree un entorno virtual de Python y actívelo:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
```

- Instale las dependencias:

```bash
$ pip install -r requirements.txt
```

- Ejecute el script `main.py`:

```bash
$ python main.py
```
