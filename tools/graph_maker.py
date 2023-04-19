from tools import ifchelper
from matplotlib import pyplot as plt

#======Descripcion general de la funcionalidad del archivo :

#Este código define varias funciones para visualizar datos de archivos IFC 
# (Industry Foundation Classes) usando gráficos de barras y gráficos circulares.
#La función get_elements_graph(file) devuelve un gráfico de barras que muestra el 
# recuento de elementos de construcción en un archivo IFC dado. La función 
# get_high_frequency_entities_graph(file) devuelve un gráfico de barras que 
# muestra la frecuencia de los tipos de entidades en un archivo IFC dado. Ambas 
# funciones utilizan la biblioteca matplotlib para crear los gráficos.
#La función load_graph(dataframe, quantity_set, quantity, user_option) utiliza la 
# biblioteca plotly para crear un gráfico circular a partir de un DataFrame que 
# contiene los datos a visualizar. Toma como argumentos un DataFrame, el conjunto 
# de cantidad de interés, la cantidad de interés y la opción de usuario para visualizar. 
# Si la cantidad de interés es "Count", la función devuelve el gráfico de barras creado 
# por get_elements_graph(file) o get_high_frequency_entities_graph(file), según el valor de quantity_set.



#======Descripcion detallada por funciones :


#El código define un diccionario llamado style que contiene una serie de parámetros 
# que definen el estilo y apariencia de las gráficas que se van a generar posteriormente.
#Entre estos parámetros, se puede destacar la figura figsize que define el tamaño de la 
# figura, los colores de fondo y borde de los ejes axes.facecolor y axes.edgecolor 
# respectivamente, y los colores de las etiquetas de los ejes axes.labelcolor. También 
# se definen los colores de fondo de la figura completa figure.facecolor y de la figura 
# guardada savefig.facecolor.
#Además, se definen el color de borde de los parches patch.edgecolor, el color de los 
# textos text.color, los colores de las marcas de los ejes xtick.color y ytick.color, y 
# el color de la rejilla grid.color.
#Por último, se definen los tamaños de fuente font.size, axes.labelsize, xtick.labelsize, 
# y ytick.labelsize para la figura.
style = {
    "figure.figsize": (8, 4.5),
    "axes.facecolor": (0.0, 0.0, 0.0, 0),
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "figure.facecolor": (0.0, 0.0, 0.0, 0),  # red   with alpha = 30%
    "savefig.facecolor": (0.0, 0.0, 0.0, 0),
    "patch.edgecolor": "#0e1117",
    "text.color": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "white",
    "font.size": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
}

#El código define una función llamada get_elements_graph que toma un archivo IFC como argumento. 
# La función utiliza la función get_types y get_type_occurence del módulo ifchelper para obtener 
# información sobre los elementos de construcción en el archivo IFC y su cantidad en el archivo. 
# Luego utiliza la función get_x_and_y de ifchelper para obtener los valores de las etiquetas y 
# las alturas de las barras del gráfico.
#Después de definir los valores de los datos para el gráfico, la función utiliza la configuración 
# de estilo previamente definida para el gráfico, y crea una figura y un objeto de ejes utilizando 
# la función subplots de matplotlib. La función bar de matplotlib se utiliza para crear el gráfico 
# de barras y se establecen varios parámetros para la apariencia del gráfico, como el título, los colores, 
# la orientación de las etiquetas y la posición de las barras. La función devuelve la figura del gráfico.
def get_elements_graph(file):
    types = ifchelper.get_types(file, "IfcBuildingElement")
    types_count = ifchelper.get_type_occurence(file, types)
    x_values, y_values = ifchelper.get_x_and_y(types_count)

    plt.rcParams.update(style)
    fig, ax = plt.subplots()
    ax.bar(x_values, y_values, width=0.5, align="center", color="red", alpha=0.5)
    ax.set_title("Building Objects Count")
    ax.tick_params(color="red", rotation=90, labelsize="7", labelcolor="red")
    ax.tick_params(axis="x", rotation=90)
    ax.set_xlabel("Element Class")
    ax.set_ylabel("Count")
    ax.xaxis.label.set_color("red")
    ax.yaxis.label.set_color("red")

    ax.set_box_aspect(aspect=1 / 2)
    ax.axis()
    # ax.xticks(y_pos, objects, rotation=90, size=10)
    return ax.figure



#La función get_high_frequency_entities_graph(file) toma un archivo IFC como 
# entrada y genera un gráfico de barras que muestra la frecuencia de los tipos 
# de entidades IFC en el archivo. Primero se llama a ifchelper.get_types(file) 
# para obtener una lista de todos los tipos de entidades en el archivo. Luego se 
# llama a ifchelper.get_type_occurence(file, types) para obtener el número de 
# ocurrencias de cada tipo de entidad en el archivo. La función también toma un 
# segundo parámetro opcional que se utiliza para filtrar solo los tipos de entidad 
# con una frecuencia de ocurrencia superior a ese número.
#Luego, la función llama a ifchelper.get_x_and_y(types_count, 400) para obtener las 
# coordenadas X e Y para el gráfico de barras. El número 400 se utiliza como segundo 
# parámetro para limitar el número de tipos de entidad a mostrar en el gráfico.
#Finalmente, la función genera el gráfico utilizando los valores X e Y obtenidos y 
# los estilos definidos en la variable style. El título del gráfico y las etiquetas 
# de los ejes también se establecen utilizando ax.set_title(), ax.set_xlabel() y ax.set_ylabel(). 
# Los colores de las etiquetas y las barras del gráfico se establecen utilizando ax.tick_params() 
# y color en el método ax.bar(). La figura resultante se devuelve como salida de la función.
def get_high_frequency_entities_graph(file):
    types = ifchelper.get_types(file)
    types_count = ifchelper.get_type_occurence(file, types)
    x_values, y_values = ifchelper.get_x_and_y(types_count, 400)

    plt.rcParams.update(style)
    fig, ax = plt.subplots()
    ax.bar(x_values, y_values, width=0.5, align="center", color="red", alpha=0.5)

    ax.set_title("IFC entity types frequency")

    ax.tick_params(color="red", rotation=90, labelsize="7", labelcolor="red")
    ax.tick_params(axis="x", rotation=90)
    ax.set_xlabel("File Entities")
    ax.set_ylabel("No of occurences")
    ax.xaxis.label.set_color("red")
    ax.yaxis.label.set_color("red")

    ax.set_box_aspect(aspect=1 / 2)
    ax.axis()
    # ax.xticks(y_pos, objects, rotation=90, size=10)
    return ax.figure




#Esta función carga un gráfico utilizando la librería Plotly Express. El gráfico 
# es un gráfico de pastel (pie chart) que muestra la distribución de una cantidad 
# específica (indicada por el parámetro quantity) en un conjunto de datos 
# (indicado por el parámetro quantity_set) especificado en un dataframe. 
# El parámetro user_option es una lista de opciones que se utilizarán para el gráfico. 
# Si la cantidad no es "Count", se utilizará una columna específica en el dataframe 
# para el valor del gráfico. La función devuelve el gráfico generado como un objeto Figure de Plotly.
def load_graph(dataframe, quantity_set, quantity, user_option):
    import plotly.express as px
    if quantity != "Count":
        column_name = f"{quantity_set}.{quantity}"
        figure_pie_chart = px.pie(
            dataframe,
            names=user_option,
            values=column_name,
        )
    return figure_pie_chart