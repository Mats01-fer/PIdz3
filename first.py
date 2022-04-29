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


title = st.text_input("connection string", value=SQL_SERVER_CONNECTION_STRING, max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=get_cinjenicne_tablice, args=None, kwargs=None,  placeholder=None, disabled=False)   



option = st.selectbox("odaberite cinjenicnu tablicu", options=[opt for opt in cinenjicne_tablice])


st.write(title)


st.subheader('Recimo tablica')
st.write(data)



# bootstrap 4 collapse example
components.html(
    """
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css"
  integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"
  integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"
  integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<div id="accordion">
  <div class="card">
    <div class="card-header" id="headingOne">
      <h5 class="mb-0">
        <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true"
          aria-controls="collapseOne">
          %s
        </button>
      </h5>
    </div>
    <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordion">
      <div class="card-body">



        <div id="accordionone">
          <div class="card">
            <div class="card-header" id="headingOneOne">
              <h5 class="mb-0">
                <button class="btn btn-link" data-toggle="collapse" data-target="#collapseOneOne" aria-expanded="true"
                  aria-controls="collapseOneOne">
                  Collapsible Group Item #1
                </button>
              </h5>
            </div>
            <div id="collapseOneOne" class="collapse" aria-labelledby="headingOneOne" data-parent="#accordionone">
              <div class="card-body">
                Collapsible Group Item #1 content
              </div>
            </div>
          </div>

        </div>



      </div>
    </div>
  </div>

</div>
    """ % (option),
    height=600,
)