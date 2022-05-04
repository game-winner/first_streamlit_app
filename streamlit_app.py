
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner!')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

#pick list to let user select fruits from the list below
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


streamlit.dataframe(fruits_to_show)

streamlit.header('FruityVice Fruit Advice')
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
  

try:
  fruit_choice = streamlit.text_input("What fruit would you like advice about?")
  if not fruit_choice:
    streamlit.error("please pick a fruit to obtain information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice) 
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()
  
#streamlit.stop()
#snowflake query

streamlit.header("The fruit load list contains: ")
def get_fruit_loadList():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")    
        return my_cur.fetchall()

if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_loadList()
    streamlit.dataframe(my_data_rows)
    
def insert_row_snowflake(this_fruit_add):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values ('my_fruit')")
        return "Thanks for adding " + this_fruit_add

fruit_add = streamlit.text_input("What fruit would you like to add?", "Banana")

if streamlit.button("Add a fruit to the list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(fruit_add)
    streamlit.text(back_from_function)
    
    
