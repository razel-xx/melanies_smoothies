# Import python packages.
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Using HTTP requests retrieive API result in JSON form. 
import requests  

# Write directly to the app.
st.title(f":cup_with_straw: Customize Your Smootie :cup_with_straw:")
st.write(
  """Choose the fruit you want in your custom **Smootie!**
  """
)

# option = st.selectbox('How would you like to be contacted?', {'Email', 'Home Phone', 'Mobile Phone'})
# st.write('You selected', option)

# option = st.selectbox('What is your favorite fruit?', {'Banana', 'Strawberry', 'Peaches'})
# st.write('You selected', option)

name_on_order = st.text_input ('Name on Smoothie', 'Input the customer name.')
st.write('The current movie title:', name_on_order)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

#st.dataframe(data=my_dataframe, use_container_width=True)
ingredient_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe)

if ingredient_list:
   # st.write(ingredient_list)
   # st.text(ingredient_list)
    
   ingredients_string = ''
   for fruit_chosen in ingredient_list:  
       ingredients_string += fruit_chosen + ' '
       #  requests retrieive API result in JSON form. 
       smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)  
       st.subheader(fruit_chosen + ' Nutritional Information')
       sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width=True)

   st.text(ingredients_string)
   
   my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""
   time_to_insert = st.button('Submit Order')
   
   if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

   st.write(my_insert_stmt)

