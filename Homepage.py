import ifcopenshell
import streamlit as st

#======Descripcion general de la funcionalidad del archivo :

# Este módulo importa la librería ifcopenshell y contiene varias 
# funciones relacionadas con la carga y manipulación de archivos 
# IFC (Industry Foundation Classes). La función callback_upload 
# se ejecuta cuando se carga un archivo IFC utilizando la función 
# st.sidebar.file_uploader. Esta función carga el archivo IFC en 
# memoria y lo convierte en un objeto ifcopenshell para su 
# posterior manipulación. La función get_project_name devuelve 
# el nombre del proyecto IFC cargado, mientras que la función 
# hange_project_name cambia el nombre del proyecto si se 
# proporciona uno nuevo. La función main es la función principal 
# que define la interfaz de usuario de la aplicación utilizando la 
# biblioteca streamlit y llama a las funciones anteriores según sea necesario.





#======Descripcion detallada por funciones :


# La función callback_upload() se ejecuta cada vez que se carga un archivo IFC y 
# se encarga de guardar información importante sobre el archivo en el estado 
# de la sesión. En concreto, la función realiza las siguientes tareas:

# 1) Almacena el nombre del archivo cargado en la variable session["file_name"].
# 2) Obtiene los datos del archivo cargado en formato bytes y los guarda en la 
#    variable session["array_buffer"].
# 3) Convierte los datos del archivo en formato de cadena (string) y luego 
#    carga el archivo en una instancia de ifcopenshell.file. La instancia de 
#    ifcopenshell.file se almacena en la variable session["ifc_file"].
# 4) Establece el valor de session["is_file_loaded"] como True para indicar 
#    que se ha cargado un archivo.
# 5) Vacia las variables en el estado de la sesión que contienen datos del 
#    archivo IFC previamente cargado, como session["isHealthDataLoaded"], 
#    session["HealthData"], session["Graphs"], session["SequenceData"], 
#    session["CostScheduleData"], session["DataFrame"], session["Classes"], 
#    session["IsDataFrameLoaded"].
def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    
    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


#La función get_project_name() devuelve el nombre del proyecto IFC que se cargó 
# en la sesión. Para hacer esto, la función utiliza la biblioteca ifcopenshell 
# para buscar en el archivo IFC cargado el objeto "IfcProject" y devolver su nombre. 
# Si el archivo IFC no se ha cargado en la sesión, esto generaría un error.
def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name





#La función change_project_name() permite al usuario cambiar el nombre del 
# proyecto cargado. Primero, se comprueba si se ha ingresado un nuevo nombre 
# en el cuadro de texto project_name_input del lado derecho de la aplicación. 
# Si es así, se cambia el nombre del proyecto en el archivo IFC cargado utilizando 
# el valor del cuadro de texto. Luego se llama a st.balloons(), que muestra un 
# efecto visual de globos que aparecen en la pantalla para indicar que se ha 
# realizado un cambio en el nombre del proyecto.
def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.balloons()


# La función main() es la función principal del programa y define la interfaz 
# de usuario utilizando la biblioteca de Streamlit.Primero, establece la 
# configuración de la página, el título y el icono de la página. Luego, muestra 
# un título y un mensaje para que el usuario cargue el archivo IFC en la barra lateral.
# La barra lateral también incluye un botón de carga de archivos y un mensaje de éxito 
# cuando se carga correctamente el archivo IFC. También incluye un campo de entrada de 
# texto para cambiar el nombre del proyecto y un botón de aplicación para confirmar el cambio.
# La barra lateral también tiene un enlace a los créditos y la licencia del programa.
# En general, la función main() define la interfaz de usuario y controla el flujo de 
# la aplicación en función de las acciones del usuario.
def main():      
    st.set_page_config(
        layout= "wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
    """ 
    ###  📁 Click on Browse File in the Side Bar to start
    """
    )

    ## Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
        st.sidebar.write("🔃 You can reload a new file  ")
        
        col1, col2 = st.columns([2,1])
        col1.subheader(f'Start Exploring "{get_project_name()}"')
        col2.text_input("✏️ Change Project Name", key="project_name_input")
        col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())

    st.sidebar.write("""
    --------------
    ### Credits:
    #### Sigma Dimensions (TM)
    
    Follow us [on Youtube](https://www.youtube.com/channel/UC9bPwuJZUD6ooKqzwdq9M9Q?sub_confirmation=1)
    
    --------------
    License: MIT
    
    """)
    st.write("")
    st.sidebar.write("")


# La función if __name__ == "__main__": es una sentencia condicional que evalúa si el 
# archivo Python está siendo ejecutado como un script principal o si ha sido importado 
# como un módulo en otro archivo Python.
# En este caso específico, si el archivo está siendo ejecutado como un script principal, 
# la variable session se inicializa como el estado de la sesión de Streamlit. La función main() 
# también se llama para mostrar la interfaz de usuario en el navegador web.
if __name__ == "__main__":
    session = st.session_state
    main()