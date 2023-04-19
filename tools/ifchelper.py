import ifcopenshell
import ifcopenshell.util.element as Element
import ifcopenshell.api
from datetime import datetime

#======Descripcion general de la funcionalidad del archivo :

# Este código utiliza la biblioteca "ifcopenshell" de Python para leer y procesar 
# datos de un modelo IFC. El código comienza definiendo una función para obtener 
# los datos de objetos por clase, la cual recorre todos los objetos en el modelo 
# IFC que coinciden con la clase especificada y recopila información relevante sobre 
# cada objeto, como su ID, nombre y ubicación. También busca y recopila información 
# sobre los conjuntos de propiedades y cantidades asociados con cada objeto.
#A continuación, hay varias funciones adicionales que se utilizan para procesar y 
# analizar los datos recopilados. Por ejemplo, hay una función para crear un marco 
# de datos de pandas a partir de los datos de los objetos recopilados anteriormente, 
# así como funciones para obtener datos específicos de tipos de objetos, tareas de 
# programación de trabajos y tareas anidadas. Finalmente, el código incluye una función 
# para formatear las fechas a un formato legible.
#En resumen, este código es útil para procesar y analizar datos de un modelo IFC 
# utilizando Python y la biblioteca ifcopenshell.



#======Descripcion detallada por funciones :


# Esta función toma un archivo y un tipo de clase como entradas y devuelve una lista de 
# diccionarios que contienen datos para todos los objetos del tipo de clase dado en el archivo. 
# Para cada objeto, la función extrae datos como ExpressId, GlobalId, Clase, Tipo predefinido, Nombre, 
# Nivel, Tipo, Conjuntos de cantidades y Conjuntos de propiedades. La función también crea un 
# conjunto de todos los atributos de conjunto de propiedades para los objetos del tipo de clase dado. 
# La función devuelve la lista de datos de objetos, así como la lista de atributos del conjunto de propiedades.
def get_objects_data_by_class(file, class_type):
    def add_pset_attributes(psets):
        for pset_name, pset_data in psets.items():
            for property_name in pset_data.keys():
                pset_attributes.add(
                    f"{pset_name}.{property_name}"
                ) if property_name != "id" else None

    objects = file.by_type(class_type)
    objects_data = []
    pset_attributes = set()

    for object in objects:
        qtos = Element.get_psets(object, qtos_only=True)
        add_pset_attributes(qtos)
        psets = Element.get_psets(object, psets_only=True)
        add_pset_attributes(psets)
        objects_data.append(
            {
                "ExpressId": object.id(),
                "GlobalId": object.GlobalId,
                "Class": object.is_a(),
                "PredefinedType": Element.get_predefined_type(object),
                "Name": object.Name,
                "Level": Element.get_container(object).Name
                if Element.get_container(object)
                else "",
                "Type": Element.get_type(object).Name
                if Element.get_type(object)
                else "",
                "QuantitySets": qtos,
                "PropertySets": psets,
            }
        )
    return objects_data, list(pset_attributes)



# Esta función recibe dos argumentos: object_data, que es un diccionario con información 
# sobre un objeto, y attribute, que es una cadena que representa un atributo del objeto.
# La función comprueba si el atributo especificado está presente directamente en object_data. 
# Si es así, se devuelve su valor. Si no, la función busca en los conjuntos de propiedades 
# (PropertySets y QuantitySets) del objeto si el atributo pertenece a alguno de ellos. 
# Si encuentra el conjunto de propiedades y el atributo en él, devuelve el valor correspondiente. 
# Si no, la función devuelve None.
# En resumen, esta función busca el valor de un atributo en un diccionario de datos de objeto y, 
# si no se encuentra directamente, busca en los conjuntos de propiedades del objeto.
def get_attribute_value(object_data, attribute):
    if "." not in attribute:
        return object_data[attribute]
    elif "." in attribute:
        pset_name = attribute.split(".", 1)[0]
        prop_name = attribute.split(".", -1)[1]
        if pset_name in object_data["PropertySets"].keys():
            if prop_name in object_data["PropertySets"][pset_name].keys():
                return object_data["PropertySets"][pset_name][prop_name]
            else:
                return None
        elif pset_name in object_data["QuantitySets"].keys():
            if prop_name in object_data["QuantitySets"][pset_name].keys():
                return object_data["QuantitySets"][pset_name][prop_name]
            else:
                return None
        else:
            return None


#La función create_pandas_dataframe crea un objeto de DataFrame de Pandas a 
# partir de una lista de objetos y un conjunto de atributos de PropertySet. 
# Los atributos de columna del DataFrame incluirán "ExpressId", "GlobalId", 
# "Class", "PredefinedType", "Name", "Level", "Type" y cualquier atributo de 
# PropertySet que se haya especificado en el conjunto de atributos pset_attributes.
# La función comienza creando una lista de attributes que incluye los atributos 
# antes mencionados junto con los atributos de PropertySet. Luego itera a través 
# de cada objeto en la lista data y crea una fila para cada uno. Para cada fila, 
# itera a través de cada atributo en la lista attributes y utiliza la función 
# get_attribute_value para obtener el valor correspondiente de cada atributo en 
# el objeto. Finalmente, agrega cada fila al objeto de datos de Pandas y 
# devuelve el DataFrame resultante.
def create_pandas_dataframe(data, pset_attributes):
    import pandas as pd

    ## List of Attributes
    attributes = [
        "ExpressId",
        "GlobalId",
        "Class",
        "PredefinedType",
        "Name",
        "Level",
        "Type",
    ] + pset_attributes
    ## Export Data to Pandas
    pandas_data = []
    for object_data in data:
        row = []
        for attribute in attributes:
            value = get_attribute_value(object_data, attribute)
            row.append(value)
        pandas_data.append(tuple(row))
    return pd.DataFrame.from_records(pandas_data, columns=attributes)




#La función get_stories recorre el modelo de datos file en busca de elementos 
# del tipo IfcBuildingStorey, y crea un diccionario para cada uno de ellos con 
# dos claves: "Storey", que contiene el nombre del elemento, y "Elevation", que 
# contiene la elevación del elemento. Estos diccionarios se agregan a una lista 
# llamada dict, que es la que se devuelve al final de la función.
def get_stories(file):
    dict = []
    for storey in file.by_type("IfcBuildingStorey"):
        dict.append({"Storey": storey.Name, "Elevation": storey.Elevation})
    return dict


#La función get_project(file) recibe como entrada un archivo en formato IFC y 
# devuelve el objeto IfcProject correspondiente al proyecto contenido en el archivo. 
# Esto se realiza mediante la función file.by_type("IfcProject")[0], que obtiene 
# todos los objetos del tipo IfcProject presentes en el archivo (que debería ser uno solo) 
# y devuelve el primero de ellos.
def get_project(file):
    return file.by_type("IfcProject")[0]



#La función get_types() devuelve un conjunto de los tipos de entidades presentes 
# en el archivo IFC cargado en file. Si se proporciona el argumento parent_class, 
# la función devuelve los tipos de entidades que son subclases de parent_class. 
# En caso contrario, la función devuelve los tipos de todas las entidades 
# presentes en el archivo IFC.
def get_types(file, parent_class=None):
    if parent_class:
        return set(i.is_a() for i in file if i.is_a(parent_class))
    else:
        return set(i.is_a() for i in file)




#La función get_type_occurence cuenta la cantidad de instancias para cada tipo de 
# elemento en un archivo IFC y devuelve un diccionario que mapea cada tipo a su 
# respectivo número de ocurrencias. Toma dos argumentos: el archivo IFC y una 
# lista de tipos de elementos para los cuales se desea contar las ocurrencias. 
# Utiliza un bucle for para iterar sobre cada tipo de elemento en la lista types, 
# cuenta la cantidad de ocurrencias usando el método by_type del archivo IFC y 
# almacena los resultados en un diccionario que se devuelve al final.
def get_type_occurence(file, types):
    return {t: len(file.by_type(t)) for t in types}


#La función create_cost_schedule utiliza la API ifcopenshell para agregar un 
# nuevo objeto "Cost Schedule" en el archivo IFC. El parámetro name es opcional 
# y se utiliza para establecer el nombre del objeto "Cost Schedule" que se creará.
def create_cost_schedule(file, name=None):
    ifcopenshell.api.run("cost.add_cost_schedule", file, name=name)


# La función create_work_schedule utiliza la biblioteca ifcopenshell para crear un 
# nuevo programa de trabajo en un archivo IFC. Toma como argumento opcional el 
# nombre del programa de trabajo a crear y lo utiliza en la función ifcopenshell.api.run() 
# con el comando sequence.add_work_schedule. Este comando ejecuta la función 
# add_work_schedule en la biblioteca ifcopenshell para crear el programa de trabajo.
def create_work_schedule(file, name=None):
    ifcopenshell.api.run("sequence.add_work_schedule", file, name=name)


#Esta función recibe un diccionario de valores y devuelve dos listas, una con las 
# claves y otra con los valores del diccionario. La lista de claves corresponde 
# al eje x y la lista de valores al eje y. Además, se puede especificar un valor 
# umbral para que solo se incluyan en las listas aquellos valores cuya frecuencia 
# sea mayor que ese valor. Por defecto, si no se especifica ningún umbral, se 
# incluyen todos los valores del diccionario en las listas.
def get_x_and_y(values, higher_then=None):
    occurences = sorted(values.items(), key=lambda kv: kv[1], reverse=True)
    if higher_then:
        occurences = [
            occurence for occurence in occurences if occurence[1] > higher_then
        ]
    x_values = [val[0] for val in occurences]
    y_values = [val[1] for val in occurences]
    return x_values, y_values



# La función get_root_tasks recibe como entrada un objeto work_schedule que 
# representa un programa de trabajo (en la notación IFC). La función devuelve 
# una lista de tareas que están directamente relacionadas con el programa de trabajo. 
# Estas tareas se consideran las "tareas raíz" del programa de trabajo, es decir, 
# las tareas que no tienen ninguna otra tarea que dependa de ellas en el programa de trabajo.
def get_root_tasks(work_schedule):
    related_objects = []
    if work_schedule.Controls:
        for rel in work_schedule.Controls:
            for obj in rel.RelatedObjects:
                if obj.is_a("IfcTask"):
                    related_objects.append(obj)
    return related_objects



# La función get_nested_tasks recibe como entrada un objeto de tipo IfcTask. 
# Esta función busca dentro del objeto de entrada todas las relaciones "IsNestedBy" 
# y retorna una lista con todos los objetos de tipo IfcTask relacionados con el objeto 
# de entrada a través de esta relación. En otras palabras, esta función busca todas las 
# tareas anidadas dentro de la tarea de entrada y las devuelve en una lista.
def get_nested_tasks(task):
    tasks = []
    for rel in task.IsNestedBy or []:
        for object in rel.RelatedObjects:
            if object.is_a("IfcTask"):
                tasks.append(object)
    return tasks



#La función get_nested_tasks2(task) es una versión abreviada de get_nested_tasks(task) 
# que utiliza una expresión de lista en lugar de un ciclo for para crear la lista de 
# tareas anidadas. En lugar de iterar sobre task.IsNestedBy, obtiene una lista de 
# RelatedObjects para cada relación en task.IsNestedBy y luego filtra aquellos que 
# son una instancia de IfcTask. En resumen, ambas funciones hacen lo mismo: devuelven 
# una lista de tareas anidadas para una tarea dada.
def get_nested_tasks2(task):
    return [object for object in [rel.RelatedObjects for rel in task.IsNestedBy] if object.is_a("IfcTask")]



#La función get_schedule_tasks(work_schedule) devuelve una lista de todas las tareas programadas 
# (objetos IfcTask) de un programa de trabajo (work_schedule) que puede incluir tareas anidadas. 
# La función primero obtiene todas las tareas principales del programa de trabajo utilizando la 
# función get_root_tasks(work_schedule) y luego, para cada tarea principal, llama a la función 
# append_tasks(task) para agregar todas las tareas anidadas en una lista llamada all_tasks. 
# La función append_tasks(task) es una función recursiva que agrega todas las tareas anidadas 
# para una tarea dada, utilizando la función get_nested_tasks(task) que devuelve una lista de 
# todas las tareas anidadas para una tarea dada.
def get_schedule_tasks(work_schedule):
    all_tasks = []
    def append_tasks(task):
        for nested_task in get_nested_tasks(task):
            all_tasks.append(nested_task)
            if nested_task.IsNestedBy:
                append_tasks(nested_task)

    root_tasks = get_root_tasks(work_schedule)
    for root_task in root_tasks:
        append_tasks(root_task)
    return all_tasks

#La función format_date_from_iso() toma una cadena de fecha en formato ISO 
# y devuelve la fecha formateada como una cadena en un formato diferente. 
# Primero convierte la cadena de fecha en formato ISO en un objeto de fecha 
# y hora utilizando el método fromisoformat() del módulo datetime. Luego, 
# utiliza el método strftime() para convertir el objeto de fecha y hora en 
# una cadena de fecha formateada según el formato especificado ("%d %b %y" en este caso). 
# Si la entrada es una cadena vacía o nula, la función devuelve una cadena vacía.
def format_date_from_iso(iso_date=None):
    return datetime.fromisoformat(iso_date).strftime('%d %b %y') if iso_date else ""




#La función get_task_data toma una lista de objetos de tareas (tasks) y devuelve una 
# lista de diccionarios que contienen información relevante sobre cada tarea. Cada 
# diccionario contiene la identificación de la tarea (Identification), el nombre 
# de la tarea (Name), la fecha de inicio planificada de la tarea (ScheduleStart) y 
# la fecha de finalización planificada de la tarea (ScheduleFinish). La fecha de 
# inicio y finalización se formatean utilizando la función format_date_from_iso que 
# convierte las fechas en formato ISO a un formato legible por humanos ('%d %b %y').
def get_task_data(tasks):
    return [
        {
            "Identification":task.Identification, 
            "Name":task.Name, 
            "ScheduleStart": format_date_from_iso(task.TaskTime.ScheduleStart) if task.TaskTime else "", 
            "ScheduleFinish": format_date_from_iso(task.TaskTime.ScheduleFinish) if task.TaskTime else "", 
        } for task in tasks
    ]




#La función format_ifcjs_psets(ifcJSON) recibe como parámetro un diccionario en 
# formato JSON que contiene información de PropertySets de un archivo IFC. La función 
# organiza los datos del JSON para que sea más fácil su manejo y devolución, creando 
# un diccionario nuevo con la información organizada.
#La función recorre los objetos pset del JSON y verifica si su nombre contiene 
# "Qto" o "Pset". Si contiene "Qto", recorre los objetos Quantities y obtiene su 
# nombre y valor. Luego, si el expressID del pset aún no está en el diccionario dict, 
# agrega la información básica del pset al diccionario (su nombre y una lista vacía 
# donde se guardarán las cantidades). Finalmente, agrega la cantidad actual a la 
# lista de cantidades correspondiente.
#Si el nombre del pset contiene "Pset", la función recorre los objetos HasProperties y 
# obtiene su nombre y valor de la misma manera que se hizo anteriormente. Luego, si el 
# expressID del pset aún no está en el diccionario dict, agrega la información básica 
# del pset al diccionario (su nombre y una lista vacía donde se guardarán las propiedades). 
# Finalmente, agrega la propiedad actual a la lista de propiedades correspondiente.
#La función devuelve el diccionario dict que contiene toda la información organizada.
def format_ifcjs_psets(ifcJSON):
    """
    Organise pset data from web-ifc-api response
    """
    dict= {}
    for pset in ifcJSON:
        if "Qto" in pset["Name"]["value"]:
            for quantity in pset["Quantities"]:
                quantity_name = quantity["Name"]["value"]
                quantity_value = ""
                for key in quantity.keys():
                    if "Value" in key:
                        quantity_value = quantity[key]["value"]
                # quantity_value = quantity[5]["value"]
                if pset["expressID"] not in dict:
                    dict[pset["expressID"]] = {
                        "Name":pset["Name"]["value"], 
                        "Data":[]
                    }
                dict[pset["expressID"]]["Data"].append({
                    "Name": quantity_name,
                    "Value": quantity_value
                })
        if "Pset" in pset["Name"]["value"]:
            for property in pset["HasProperties"]:
                property_name = property["Name"]["value"]
                property_value = ""
                for key in property.keys():
                    if "Value" in key:
                        property_value = property[key]["value"]
                # property_value = property[5]["value"]
                if pset["expressID"] not in dict:
                    dict[pset["expressID"]] = {
                        "Name":pset["Name"]["value"], 
                        "Data":[]
                    }
                dict[pset["expressID"]]["Data"].append({
                    "Name": property_name,
                    "Value": property_value
                })
    return dict
