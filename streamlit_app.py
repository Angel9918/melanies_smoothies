# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

# Agregar un textbox para que el usuario pueda ingresar su nombre
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your smoothie will be:', name_on_order)

# Acceder a la sesion que se encuentra activa para consultar las tablas
cnx = st.connection("snowflake")
session = cnx.session()

# Consultar la tabla de ingredientes desde la base de Smoothies para mostrar como opciones
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# st.dataframe(data=my_dataframe, use_container_width=True)

# Activar una opcion de opcion multiple para los ingredientes que se quieren agregar
ingredients_list = st.multiselect (
    'Choose up to 5 ingredients:'
    , my_dataframe
    , max_selections= 5
)

# Muestra la lista de ingredientes seleccionados solo cuando exista al menos un registro para mostrar
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)

    # Se crea con el fin de pasar la lista de ingredientes como un string y no como una lista
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
    # st.write(ingredients_string)

    # Se crea la tabla que almacenará los registros de ordenes directamente en Snowflake
    # Se realiza una sentencia para agregar los ingredientes a la tabla
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+ name_on_order +"""')"""

    #st.write(my_insert_stmt)

    # Permite realizar el debugging de la consulta antes de que se ejecute en la base
    #st.stop()
    
    time_to_insert = st.button('Submit Order')

    # Se verifica que la lista exista y se ejecuta el insert de la orden
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+ name_on_order+'!', icon="✅")
        

# New section to display smoothiefroot nutrition information    
import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

