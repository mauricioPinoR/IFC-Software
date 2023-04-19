import streamlit as st
from tools import ifchelper
import json
import ifcopenshell
##################### STREAMLIT IFC-JS COMPONENT MAGIC ######################
from pathlib import Path                                                    #
from re import L                                                            #
from typing import Optional                                                 #
import streamlit.components.v1 as components                                #
#                                                                           #
#                                                                           #
# Tell streamlit that there is a component called ifc_js_viewer,            #
# and that the code to display that component is in the "frontend" folder   #
frontend_dir = (Path(__file__).parent / "frontend-viewer").absolute()       #
_component_func = components.declare_component(                             #
	"ifc_js_viewer", path=str(frontend_dir)                                 #
)                                                                           #
#                                                                           #
# Create the python function that will be called                            #
def ifc_js_viewer(                                                          #    
    url: Optional[str] = None,                                              #
):                                                                          #
    component_value = _component_func(                                      #
        url=url,                                                            #
    )                                                                       #
    return component_value                                                  #
#                                                                           #
#############################################################################


#======Descripcion general de la funcionalidad del archivo :


#Este archivo de Python parece ser un módulo que utiliza la biblioteca Streamlit 
# para interactuar con modelos IFC (Industry Foundation Classes) a través de una 
# interfaz web. El código define funciones para visualizar y analizar los datos del 
# modelo IFC utilizando un visor JavaScript incorporado en la página web.
#El módulo importa varios paquetes y bibliotecas de Python, incluyendo streamlit, json, 
# ifcopenshell, pathlib, re, typing, y streamlit.components.v1. También importa una 
# biblioteca personalizada llamada tools.ifchelper.
#El código declara un componente ifc_js_viewer utilizando streamlit.components.v1, que 
# se utiliza para visualizar modelos IFC en formato JSON utilizando un componente JavaScript 
# en el frontend de la aplicación web.
# El módulo define varias funciones, incluyendo draw_3d_viewer para dibujar el visor 3D en 
# la interfaz de usuario, get_psets_from_ifc_js para extraer la información de propiedades 
# del objeto IFC del visor JavaScript, format_ifc_js_psets para formatear las propiedades del 
# objeto en un formato legible, y get_object_data para extraer información sobre un objeto IFC 
# específico en el modelo.
#Además, el módulo también define funciones para editar información de objetos IFC, como 
# edit_object_data, así como funciones para mostrar información de salud y depuración del modelo.



#======Descripcion detallada por funciones :


#La función draw_3d_viewer() parece ser una función que se utiliza para cargar y visualizar 
# modelos BIM (Building Information Modeling) en 3D en un entorno de aplicación web.
#La función anidada get_current_ifc_file() devuelve el archivo IFC (Industry Foundation Classes) 
# actual en formato de búfer de matriz (array buffer), que se utiliza como entrada para la 
# función ifc_js_viewer().
#La función ifc_js_viewer() parece ser una función de JavaScript que se utiliza para renderizar 
# el modelo BIM en un visor 3D en el navegador web. La salida de esta función se almacena en la 
# variable session.ifc_js_response.
#Finalmente, la función muestra un mensaje de éxito en la barra lateral del panel de la aplicación 
# web mediante el método st.sidebar.success().
def draw_3d_viewer():
    def get_current_ifc_file():
        return session.array_buffer
    session.ifc_js_response = ifc_js_viewer(get_current_ifc_file())
    st.sidebar.success("Visualiser loaded")


#Esta función obtiene los Property Sets (Psets) de un modelo IFC en formato JSON 
# que se ha cargado previamente utilizando la función ifc_js_viewer(). Si la respuesta 
# de ifc_js_viewer() está presente en session.ifc_js_response, la función convierte la 
# respuesta JSON en un objeto Python mediante json.loads() y lo devuelve. Si la respuesta 
# no está presente, la función devuelve None.
def get_psets_from_ifc_js():
    if session.ifc_js_response:
        return json.loads(session.ifc_js_response)
        

#La función format_ifc_js_psets(data) parece que formatea los datos de 
# propiedades y conjuntos de propiedades (psets) que se obtuvieron a 
# través de la función get_psets_from_ifc_js() para que puedan ser visualizados 
# en la aplicación web. Es probable que ifchelper sea un módulo que contiene 
# funciones de ayuda para procesar y formatear los datos IFC. Sin conocer el 
# código de la función format_ifc_js_psets(), no es posible saber con exactitud 
# qué operaciones específicas realiza.
def format_ifc_js_psets(data):
    return ifchelper.format_ifcjs_psets(data)


# Esta función inicializa un objeto de propiedades de depuración en la sesión 
# si aún no existe. También tiene un parámetro de fuerza opcional que, si se 
# establece en True, sobrescribirá cualquier propiedad de depuración existente 
# en la sesión con un nuevo objeto. El objeto de propiedades de depuración 
# contiene varios atributos, como step_id, number_of_polygons, active_step_id, 
# atributos, etc., que se utilizan para depurar y analizar los datos.
def initialise_debug_props(force=False):
    if not "BIMDebugProperties" in session:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }
    if force:
        session.BIMDebugProperties = {
            "step_id": 0,
            "number_of_polygons": 0,
            "percentile_of_polygons": 0,
            "active_step_id": 0,
            "step_id_breadcrumb": [],
            "attributes": [],
            "inverse_attributes": [],
            "inverse_references": [],
            "express_file": None,
        }



#La función get_object_data() recupera información sobre un objeto en 
# particular en un archivo IFC y la almacena en la variable session.BIMDebugProperties. 
# La función toma un parámetro opcional fromId que especifica el ID del objeto 
# para recuperar información. Si no se proporciona fromId, la función recupera 
# información sobre el objeto almacenado en session.object_id. La información 
# recuperada incluye los atributos del objeto, los atributos inversos del objeto 
# y las referencias inversas del objeto. La función add_attribute() es una función 
# anidada que se usa para agregar atributos al diccionario debug_props. La función 
# también imprime el valor de los atributos del diccionario debug_props.
def get_object_data(fromId=None):
    def add_attribute(prop, key, value):
        if isinstance(value, tuple) and len(value) < 10:
            for i, item in enumerate(value):
                add_attribute(prop, key + f"[{i}]", item)
            return
        elif isinstance(value, tuple) and len(value) >= 10:
            key = key + "({})".format(len(value))
        
        propy = {
            "name": key,
            "string_value": str(value),
            "int_value": int(value.id()) if isinstance(value, ifcopenshell.entity_instance) else None,
        }
        prop.append(propy)
            
    if session.BIMDebugProperties:
        initialise_debug_props(force=True)
        step_id = 0
        if fromId:
            step_id =  int(fromId)
        else:
            step_id = int(session.object_id) if session.object_id else 0
        debug_props = st.session_state.BIMDebugProperties
        debug_props["active_step_id"] = step_id
        
        crumb = {"name": str(step_id)}
        debug_props["step_id_breadcrumb"].append(crumb)
        element = session.ifc_file.by_id(step_id)
        debug_props["inverse_attributes"] = []
        debug_props["inverse_references"] = []
        
        if element:
        
            for key, value in element.get_info().items():
                add_attribute(debug_props["attributes"], key, value)

            for key in dir(element):
                if (
                    not key[0].isalpha()
                    or key[0] != key[0].upper()
                    or key in element.get_info()
                    or not getattr(element, key)
                ):
                    continue
                add_attribute(debug_props["inverse_attributes"], key, getattr(element, key))
            
            for inverse in session.ifc_file.get_inverse(element):
                propy = {
                    "string_value": str(inverse),
                    "int_value": inverse.id(),
                }
                debug_props["inverse_references"].append(propy)
                
            print(debug_props["attributes"])




#Esta función recibe dos parámetros: el primero es el object_id de un 
# elemento del archivo IFC que se va a editar, y el segundo es el 
# nombre de un atributo de ese elemento que se desea editar. La función 
# busca el elemento en el archivo IFC utilizando su object_id y luego 
# imprime en la consola el valor actual del atributo especificado mediante 
# la función getattr(). En resumen, esta función se encarga de mostrar el 
# valor actual de un atributo de un elemento del archivo IFC.
def edit_object_data(object_id, attribute):
    entity = session.ifc_file.by_id(object_id)
    print(getattr(entity, attribute))
    

#=============IMPORTANTE=====================================================================

#La función write_pset_data es responsable de escribir los datos de los Property 
# Sets (conjuntos de propiedades) de los objetos seleccionados en la vista 3D en 
# la aplicación. Primero, se llama a la función get_psets_from_ifc_js() para 
# obtener los Property Sets de los objetos seleccionados. Si se obtienen datos, 
# se formatean utilizando la función format_ifc_js_psets y se imprimen en una 
# tabla utilizando la función st.table() de la biblioteca Streamlit. El nombre 
# del Property Set se utiliza como encabezado de la subsección y se visualiza 
# con st.subheader().
def write_pset_data():
    data = get_psets_from_ifc_js()
    if data:
        st.subheader("🧮 Object Properties")
        psets = format_ifc_js_psets(data['props'])
        for pset in psets.values():
            st.subheader(pset["Name"])
            st.table(pset["Data"])    


#La función write_health_data se encarga de mostrar un panel de depuración con 
# información sobre el objeto seleccionado. El panel contiene tres secciones: 
# "Propiedades del objeto", "Atributos" y "Atributos inversos". 
# En la sección "Propiedades del objeto", el usuario puede ingresar una 
# ID de objeto o usar un botón para inspeccionar las propiedades del objeto 
# desde el modelo. En la sección "Atributos", se muestra una tabla con los 
# atributos del objeto seleccionado. El usuario puede editar los valores de 
# los atributos en esta sección. En la sección "Atributos inversos", se muestran 
# los atributos inversos del objeto seleccionado. También hay una sección para 
# "Referencias inversas", que muestra una lista de objetos que hacen referencia 
# al objeto seleccionado. Para cada objeto, hay un botón que permite al usuario 
# inspeccionar las propiedades del objeto. 
def write_health_data():
    st.subheader("🩺 Debugger")
    ## REPLICATE IFC DEBUG PANNEL
    row1_col1, row1_col2 = st.columns([1,5])
    with row1_col1:
        st.number_input("Object ID", key="object_id")
    with row1_col2:
        st.button("Inspect From Id", key="edit_object_button", on_click=get_object_data, args=(st.session_state.object_id,))
        data = get_psets_from_ifc_js()
        if data:
            st.button("Inspect from Model", key="get_object_button", on_click=get_object_data, args=(data['id'],)) if data else ""

    if "BIMDebugProperties" in session and session.BIMDebugProperties:
        props = session.BIMDebugProperties
        if props["attributes"]:
            st.subheader("Attributes")
            # st.table(props["attributes"])
            for prop in props["attributes"]:
                col2, col3 = st.columns([3,3])
                if prop["int_value"]:
                    col2.text(f'🔗 {prop["name"]}')
                    col2.info(prop["string_value"])
                    col3.write("🔗")
                    col3.button("Get Object", key=f'get_object_pop_button_{prop["int_value"]}', on_click=get_object_data, args=(prop["int_value"],))
                else:
                    col2.text_input(label=prop["name"], key=prop["name"], value=prop["string_value"])
                    # col3.button("Edit Object", key=f'edit_object_{prop["name"]}', on_click=edit_object_data, args=(props["active_step_id"],prop["name"]))
                    
        if props["inverse_attributes"]:
            st.subheader("Inverse Attributes")
            for inverse in props["inverse_attributes"]:
                col1, col2, col3 = st.columns([3,5,8])
                col1.text(inverse["name"])
                col2.text(inverse["string_value"])
                if inverse["int_value"]:
                    col3.button("Get Object", key=f'get_object_pop_button_{inverse["int_value"]}', on_click=get_object_data, args=(inverse["int_value"],))
        
        ## draw inverse references
        if props["inverse_references"]:
            st.subheader("Inverse References")
            for inverse in props["inverse_references"]:
                col1, col3 = st.columns([3,3])
                col1.text(inverse["string_value"])
                if inverse["int_value"]:
                    col3.button("Get Object", key=f'get_object_pop_button_inverse_{inverse["int_value"]}', on_click=get_object_data, args=(inverse["int_value"],))
            


#Esta función es la función principal del script y se encarga de ejecutar 
# todo el proceso. En primer lugar, llama a la función initialise_debug_props() 
# para inicializar las propiedades de depuración. Luego, dibuja el encabezado 
# de la página y verifica si existe un archivo IFC en la sesión. Si existe un 
# archivo IFC, llama a la función draw_3d_viewer() para dibujar el visor 3D y 
# crea dos pestañas llamadas "Properties" y "Debugger". Luego, llama a la 
# función write_pset_data() dentro de la pestaña "Properties" para escribir 
# los datos de las propiedades de los objetos y llama a la función write_health_data() 
# dentro de la pestaña "Debugger" para escribir los datos de depuración. Si no hay un 
# archivo IFC en la sesión, muestra una cabecera que indica que el usuario debe cargar 
# un archivo desde la página de inicio.    
def execute():
    initialise_debug_props()
    st.header("🎮 IFC.js Viewer")
    if "ifc_file" in session and session["ifc_file"]:
        if "ifc_js_response" not in session:
            session["ifc_js_response"] = ""
        draw_3d_viewer()
        tab1, tab2 = st.tabs(["🧮 Properties", "🩺 Debugger"])
        with tab1:
            write_pset_data()
        with tab2:
            write_health_data()
    else:
        st.header("Step 1: Load a file from the Home Page")
session = st.session_state
execute()