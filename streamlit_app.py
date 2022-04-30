
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLerror

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
fruit_choice = streamlit.text_input("What fruit would you like advice about?", "Kiwi")
streamlit.write("You have entered: " + fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

streamlit.dataframe(fruityvice_normalized)

streamlit.stop()
#snowflake query
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains: ")
streamlit.dataframe(my_data_rows)

fruit_add = streamlit.text_input("What fruit would you like to add?", "Banana")
streamlit.write("Thanks for adding " + fruit_add)

my_cur.execute("insert into fruit_load_list values ('from streamlit') ")
