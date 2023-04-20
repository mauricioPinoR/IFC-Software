import streamlit as st
from tools import ifchelper
from tools import pandashelper
from tools import graph_maker

#======Descripcion general de la funcionalidad del archivo :

#Este módulo contiene una aplicación web que permite cargar y analizar datos en 
# formato IFC (Industry Foundation Classes) que representan modelos de edificios 
# en 3D. El módulo utiliza la biblioteca Streamlit para crear la interfaz gráfica 
# de usuario y las herramientas de visualización de datos. El código define varias 
# funciones que se encargan de cargar y procesar los datos IFC, así como de generar 
# tablas y gráficos para visualizar los resultados.
#La función initialize_session_state() se utiliza para crear una sesión y establecer 
# los valores iniciales de algunas variables. La función load_data() se encarga de 
# cargar los datos IFC en un marco de datos de Pandas y de actualizar la variable 
# de sesión IsDataFrameLoaded en consecuencia. La función download_csv() y download_excel() 
# descargan los datos del marco de datos en formato CSV y Excel, respectivamente.
#La función execute() es el punto de entrada principal del código. En esta función se 
# configura la página, se muestra un encabezado y se verifica si los datos IFC han 
# sido cargados. Si los datos no han sido cargados, se llama a la función load_data() para 
# cargarlos. Si los datos están cargados, se muestra una pestaña para revisar el marco de 
# datos y otra pestaña para revisar los totales y gráficos de los datos cuantitativos. La 
# función pandashelper.filter_dataframe_per_class() se utiliza para filtrar el marco de datos 
# por clase y la función pandashelper.get_quantities() se utiliza para obtener las cantidades 
# cuantitativas. La biblioteca Plotly se utiliza para generar los gráficos.




session = st.session_state

def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def load_data():
    if "ifc_file" in session:
        session["DataFrame"] = get_ifc_pandas()
        session.Classes = session.DataFrame["Class"].value_counts().keys().tolist()
        session["IsDataFrameLoaded"] = True

def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file, 
        "IfcBuildingElement"
    )
    frame = ifchelper.create_pandas_dataframe(data, pset_attributes)
    return frame

def download_csv():
    pandashelper.download_csv(session.file_name,session.DataFrame)

def download_excel():
    pandashelper.download_excel(session.file_name,session.DataFrame)

def execute():  
    st.set_page_config(
        page_title="Quantities",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header(" 🧮 Model Quantities")
    if not "IsDataFrameLoaded" in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:    
        tab1, tab2 = st.tabs(["Dataframe Utilities", "Quantities Review"])
        with tab1:
            ## DATAFRAME REVIEW            
            st.header("DataFrame Review")  
            st.write(session.DataFrame)
            # from st_aggrid import AgGrid
            # AgGrid(session.DataFrame)
            st.button("Download CSV", key="download_csv", on_click=download_csv)
            st.button("Download Excel", key="download_excel", on_click=download_excel)
        with tab2:
            row2col1, row2col2 = st.columns(2)
            with row2col1:
                if session.IsDataFrameLoaded:
                    class_selector = st.selectbox("Select Class", session.Classes, key="class_selector")
                    session["filtered_frame"] = pandashelper.filter_dataframe_per_class(session.DataFrame, session.class_selector)
                    session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame"])
                    if session["qtos"] is not None:
                        qto_selector = st.selectbox("Select Quantity Set", session.qtos, key='qto_selector')
                        quantities = pandashelper.get_quantities(session.filtered_frame, session.qto_selector)
                        st.selectbox("Select Quantity", quantities, key="quantity_selector")
                        st.radio('Split per', ['Level', 'Type'], key="split_options")
                    else:
                        st.warning("No Quantities to Look at !")
            ## DRAW FRAME
            with row2col2: 
                if "quantity_selector" in session and session.quantity_selector == "Count":
                    total = pandashelper.get_total(session.filtered_frame)
                    st.write(f"The total number of {session.class_selector} is {total}")
                else:
                    if session.qtos is not None:
                        st.subheader(f"{session.class_selector} {session.quantity_selector}")
                        graph = graph_maker.load_graph(
                            session.filtered_frame,
                            session.qto_selector,
                            session.quantity_selector,
                            session.split_options,                                
                        )
                        st.plotly_chart(graph)
    else: 
        st.header("Step 1: Load a file from the Home Page")
    
execute()