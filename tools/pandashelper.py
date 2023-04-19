
CLASS = "Class"
LEVEL = "Level"

#======Descripcion general de la funcionalidad del archivo :

#Este archivo contiene varias funciones para procesar y filtrar un dataframe que 
#contiene información sobre objetos de construcción.
#La función filter_dataframe_per_class(dataframe, class_name) filtra el dataframe 
# para seleccionar solo las filas que pertenecen a una clase específica.
#La función get_total(dataframe) devuelve el número total de filas en el dataframe.
#La función get_qsets_columns(dataframe) devuelve una lista de columnas en el dataframe 
#que representan conjuntos de cantidades.
#La función get_quantities(frame, quantity_set) devuelve una lista de columnas en el 
# dataframe que representan una determinada cantidad en un conjunto de cantidades dado.
#Las funciones download_csv(file_name, dataframe) y download_excel(file_name, dataframe) 
# descargan el dataframe como un archivo CSV o Excel en la carpeta de descargas.



#======Descripcion detallada por funciones :


#La función filter_dataframe_per_class recibe un dataframe y un nombre de clase como 
# argumentos, y devuelve un nuevo dataframe que contiene solo las filas en las que la 
# columna "Class" coincide con el nombre de clase proporcionado. Además, elimina todas 
# las columnas que contienen solo valores nulos. En resumen, la función filtra el dataframe 
# original por la clase de objeto especificada y devuelve un dataframe más pequeño y limpio 
# que solo contiene información relevante.
def filter_dataframe_per_class(dataframe, class_name):
    return dataframe[dataframe["Class"] == class_name].dropna(axis=1, how="all")



# La función get_total recibe como entrada un DataFrame "dataframe" y retorna el número total 
# de instancias de la clase "Class" en el DataFrame. Primero, la función utiliza el 
# método value_counts() de Pandas para contar el número de veces que aparece cada valor 
# en la columna "Class". Luego, suma todos los valores contados para obtener el número 
# total de instancias de la clase "Class". Finalmente, retorna el valor total.
def get_total(dataframe):
    count = dataframe[CLASS].value_counts().sum()
    return count


#La función get_qsets_columns recibe un dataframe y devuelve una lista de las columnas 
# que representan conjuntos de cantidades (quantity sets).Primero, la función crea un 
# conjunto vacío qset_columns. Luego, itera sobre todas las columnas del dataframe y 
# si la cadena "Qto" se encuentra en el nombre de la columna, se divide el nombre de 
# la columna por el primer punto que se encuentra en la cadena y se agrega el resultado 
# al conjunto qset_columns.
#Finalmente, si el conjunto qset_columns está vacío, se devuelve None; de lo contrario, 
# se devuelve una lista de los elementos del conjunto.
def get_qsets_columns(dataframe):
    qset_columns = set()
    [qset_columns.add(column.split(".", 1)[0]) for column in dataframe.columns if "Qto" in column]
    return list(qset_columns) if qset_columns else None



#La función get_quantities toma un DataFrame frame y un conjunto de cantidades quantity_set 
# como entrada y devuelve una lista de nombres de columnas que corresponden a las cantidades 
# de quantity_set presentes en el DataFrame frame. La función divide cada nombre de columna 
# en dos partes utilizando el separador ".", y solo agrega la segunda parte a la lista de 
# columnas si la primera parte es igual a quantity_set. La función también agrega "Count" 
# al final de la lista de columnas.
def get_quantities(frame, quantity_set):
    columns = []
    [columns.append(column.split(".", 1)[1]) for column in frame.columns if quantity_set in column]
    columns.append("Count")
    return columns



#La función download_csv toma un nombre de archivo y un objeto DataFrame como argumentos. 
# Primero, reemplaza cualquier extensión de archivo .ifc en el nombre de archivo con la 
# extensión .csv. Luego, guarda el objeto DataFrame en formato CSV en un archivo con el 
# nombre modificado en la ruta ./downloads/.
def download_csv(file_name, dataframe):
    file_name = file_name.replace('.ifc', '.csv')
    dataframe.to_csv(f'./downloads/{file_name}')




#La función download_excel toma como entrada un nombre de archivo y un marco de datos de pandas, 
# y guarda los datos del marco de datos en un archivo de Excel en la carpeta "descargas". 
# Primero, cambia la extensión del archivo de .ifc a .xlsx. Luego, utiliza la biblioteca 
# pandas para crear un objeto ExcelWriter que permite escribir datos en un archivo de Excel. 
# A continuación, itera sobre cada valor único en la columna Class del marco de datos y crea un 
# nuevo marco de datos que contiene solo las filas de ese valor de Class. Este marco de datos se 
# guarda en una hoja de cálculo separada en el archivo de Excel con el nombre de la clase. Finalmente, 
# se guarda el archivo de Excel y se cierra el objeto ExcelWriter.
def download_excel(file_name, dataframe):
    import pandas
    file_name = file_name.replace('.ifc', '.xlsx')
    writer = pandas.ExcelWriter(f'./downloads/{file_name}', engine="xlsxwriter") ## pip install xlsxwriter
    for object_class in dataframe[CLASS].unique():
        df_class = dataframe[dataframe[CLASS] == object_class].dropna(axis=1, how="all")
        df_class.to_excel(writer, sheet_name=object_class)
    writer.save()