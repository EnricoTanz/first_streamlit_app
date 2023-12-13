import streamlit
import pandas
import snowflake.connector 
import requests
from urllib.error import URLError

streamlit.title("My Parents New Healthy Diner")
streamlit.header('Breakfast Favorites')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text(' 🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

   
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
streamlit.dataframe(my_fruit_list)

# Let's put a pick list here so they can pick the fruit they want to include 
streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))

# Display the table on the page.
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected= streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruit_choice2 = streamlit.text_input('What fruit would you like to destroy?','Jackfruit')
streamlit.write('The user entered ', fruit_choice2)

streamlit.header("Fruityvice Fruit Advice!")

def get_fr_data(this_fruit_choice):
   fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon"+ this_fruit_choice)
   fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
   return fruityvice_normalized







try:
   fruit_choice = streamlit.text_input('What fruit would you like information about?')
   if not fruit_choice:
      streamlit.error("Fruit required")
   else:
      back_from_function= get_fr_data(fruit_choice)
      streamlit.dataframe(back_from_function)


except URLError as e:
   streamlit.error()


streamlit.header("the fruit list contains:")
def get_fruit_load_list():
   with my_cnx.cursor() as my_cur:
      my_cur.execute("select * from frui_load_list")
      return my_cur.fetchall()
      
if streamlit.button('Get fruit load list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_data_rows =get_fruit_load_list()
   streamlit.dataframe(my_data_rows)


def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("insert into fruit_load_list values ('from streamlit')")
      return "Thanks for adding" + new_fruit

add_my_fruit= streamlit.textinput("what to add?")
if streamlit.button('Add a fruit to the list'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function= insert_row_snowflake(add_my_fruit)
   streamlit.text(back_from_function)
   
   


 




