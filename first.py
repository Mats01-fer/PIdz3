from unittest import result
from soupsieve import select
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
        data_load_state.text('')
    except Exception as e:
        data_load_state.text('there was an error!')
    
    print(results)

    # data = pd.DataFrame(results, columns = ['id','func'])
    data = pd.DataFrame(results)
    print(data)
  

def run_query():
    global option, limit, use_limit
    code = "SELECT TOP %d  * FROM %s " % (limit, option) if use_limit else "SELECT * FROM %s " % option
    execute_req(code)
  
def execute_req(naredba):    
    global code_block, data
    re_result = re.search(r"Server=(.+);Database=(.+);User Id=(.+);Password=(.+);", title)
    server = re_result.group(1)
    user = re_result.group(3)
    database = re_result.group(2)
    password = re_result.group(4)
    results = []
    
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        cursor.execute(naredba)
        row = cursor.fetchone()
        while row:
            results.append(row)
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
    
    code_block = st.code(naredba, language='sql')
    st.subheader('Recimo tablica')
    st.write(data)
  
  

data_load_state = st.text('')
get_cinjenicne_tablice()


title = st.sidebar.text_input("connection string", value=SQL_SERVER_CONNECTION_STRING, max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=get_cinjenicne_tablice, args=None, kwargs=None,  placeholder=None, disabled=False)   



option = st.sidebar.selectbox("odaberite cinjenicnu tablicu", options=[opt.strip() for opt in cinenjicne_tablice])



mjere = {'mjera1': False, 'mjera2': False}
with st.sidebar.expander("Mjere"):
    for k in mjere.keys():
        mjere[k] = st.checkbox(k)
        
dimenzije = {'dimenzija1': {'attr1': False, 'attr2': False}, 'dimenzija2': {'2attr1': False, '2 attr2': False}}
with st.sidebar.expander("Dimenzije"):
    for k in dimenzije.keys():
        st.write(k)
        try:
            for k2 in dimenzije[k].keys():
                dimenzije[k][k2] = st.checkbox(k + " " + k2)
        except:
            st.write("vise atributa ima isto ime")
                




use_limit = st.sidebar.checkbox("use limit")
limit = st.sidebar.slider('limit', 0, 100, 10)


st.sidebar.button('Pokreni', on_click=run_query)


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