from unittest import result
import streamlit as st
import pandas as pd
import numpy as np
import pymssql


server = "localhost"
user = "sa"
password = "Strong.Pwd-123"




st.title('Some data')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')


@st.cache
def load_data():    
    conn = pymssql.connect(server, user, password, "dz03")
    naredba = """SELECT * from agrFun af;"""
    cursor = conn.cursor()
    cursor.execute(naredba)
    row = cursor.fetchone()
    results = []
    while row:
        print("jedan=%d, dva=%s" % (row[0], row[1]))
        row = cursor.fetchone()
        results.append(row)
    cursor.close()
    # conn.commit()
    conn.close()
    
    
    # data = pd.read_csv(DATA_URL, nrows=nrows)
    # lowercase = lambda x: str(x).lower()
    # data.rename(lowercase, axis='columns', inplace=True)
    # data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    data = pd.DataFrame(results, columns = ['id','func'])
    print(data)
    return data
  
  
# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data()
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')


st.subheader('Recimo tablica')
st.write(data)