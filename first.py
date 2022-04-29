from unittest import result
import streamlit as st
import pandas as pd
import numpy as np
import pymssql
import re
import streamlit.components.v1 as components






server = "localhost"
user = "sa"
password = "Strong.Pwd-123"
database = 'AdventureWorksDW2019'
SQL_SERVER_CONNECTION_STRING = 'Server=%s;Database=%s;User Id=%s;Password=%s;' % (server, database, user, password)




st.title('Some data')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')



cinenjicne_tablice = []
option = ""
title = SQL_SERVER_CONNECTION_STRING



# @st.cache
def get_cinjenicne_tablice():    
    global title, cinenjicne_tablice
    re_result = re.search(r"Server=(.+);Database=(.+);User Id=(.+);Password=(.+);", title)
    server = re_result.group(1)
    user = re_result.group(3)
    database = re_result.group(2)
    password = re_result.group(4)
    results = []
    
    try:
        conn = pymssql.connect(server, user, password, database)
        naredba = """SELECT *  FROM tablica WHERE sifTipTablica = 1 """ # vraca cinjenicne tablice
        cursor = conn.cursor()
        cursor.execute(naredba)
        row = cursor.fetchone()
        while row:
            results.append(row)
            cinenjicne_tablice.append(row[2])
            row = cursor.fetchone()
        cursor.close()
        # conn.commit()
        conn.close()
        data_load_state.text('Loading data...done!')
    except Exception as e:
        data_load_state.text('there was an error!')
    
    print(results)

    # data = pd.DataFrame(results, columns = ['id','func'])
    data = pd.DataFrame(results)
    print(data)
    return data
  
  
  



# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = get_cinjenicne_tablice()
# Notify the reader that the data was successfully loaded.
# data_load_state.text('Loading data...done!')


title = st.sidebar.text_input("connection string", value=SQL_SERVER_CONNECTION_STRING, max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=get_cinjenicne_tablice, args=None, kwargs=None,  placeholder=None, disabled=False)   



option = st.sidebar.selectbox("odaberite cinjenicnu tablicu", options=[opt for opt in cinenjicne_tablice])


st.sidebar.write(title)

st.subheader('Recimo tablica')
st.write(data)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
        width: 500px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {
        width: 500px;
        margin-left: -500px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)