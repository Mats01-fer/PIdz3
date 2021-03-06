from cProfile import run
from pprint import pprint
from tokenize import group
from certifi import where
import streamlit as st
import pandas as pd

from sql_utils import execute_query


server = "localhost"
user = "sa"
password = "Strong.Pwd-123"
database = 'AdventureWorksDW2019'
SQL_SERVER_CONNECTION_STRING = 'Server=%s;Database=%s;User Id=%s;Password=%s;' % (server, database, user, password)




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


cinjenicne_tablice = []
cinjenicne_tablice_id = []
option = ""
connection_string = SQL_SERVER_CONNECTION_STRING

tablice = {}




# @st.cache
def get_cinjenicne_tablice():    
    global connection_string, cinjenicne_tablice, cinjenicne_tablice_id


    # 1. Dohvati popis cinjenicnih tablica
    naredba = """SELECT *  FROM tablica WHERE sifTipTablica = 1 """
    (results, _) = execute_query(naredba, connection_string)    

    cinjenicne_tablice = [i[2].strip() for i in results]
    cinjenicne_tablice_id = [i[0] for i in results]
    
    for tablica in cinjenicne_tablice:
        tablice[tablica] = {'mjere': {}, 'dimenzije': {}}
    
    # 2. za svaku tablicu dohvati popis mjera    
    for tablica in cinjenicne_tablice:
        curr_id = cinjenicne_tablice_id[cinjenicne_tablice.index(tablica)]
    
        naredba = """SELECT  nazAgrFun, imeSQLAtrib, tabAtributAgrFun.imeAtrib 
            FROM tabAtribut, agrFun, tablica, tabAtributAgrFun                                          
            WHERE tabAtribut.sifTablica = tablica.sifTablica 
            AND tabAtribut.sifTablica =  %s 
            AND tabAtribut.sifTablica  = tabAtributAgrFun.sifTablica 
            AND tabAtribut.rbrAtrib  = tabAtributAgrFun.rbrAtrib 
            AND tabAtributAgrFun.sifAgrFun = agrFun.sifAgrFun 
            AND tabAtribut.sifTipAtrib = 1
            ORDER BY tabAtribut.rbrAtrib""" % curr_id
        
        (results, _) = execute_query(naredba, connection_string)
        
        for i in results:
            tablice[tablica]['mjere'][i[2].strip()] = {'active': False, 'naredba': "%s(%s)" % (i[0].strip(), i[1].strip())}
            
            
    # 3. za svaku tablicu dohvati popis dimenzija
    for tablica in cinjenicne_tablice:
        curr_id = cinjenicne_tablice_id[cinjenicne_tablice.index(tablica)]
        
        naredba = """SELECT   dimTablica.nazTablica
                    , tabAtribut.imeSQLAtrib
                    , dimTabAtribut.imeSqlAtrib
                    , dimTablica.nazSQLTablica  AS nazSqlDimTablica
                    , cinjTablica.nazSQLTablica AS nazSqlCinjTablica
                    
                    , tabAtribut.*
                FROM tabAtribut, dimCinj
                    , tablica dimTablica, tablica cinjTablica 
                    , tabAtribut cinjTabAtribut, tabAtribut dimTabAtribut
                WHERE dimCinj.sifDimTablica  = dimTablica.sifTablica
                AND dimCinj.sifCinjTablica = cinjTablica.sifTablica

                AND dimCinj.sifCinjTablica = cinjTabAtribut.sifTablica
                AND dimCinj.rbrCinj = cinjTabAtribut.rbrAtrib

                AND dimCinj.sifDimTablica = dimTabAtribut.sifTablica
                AND dimCinj.rbrDim = dimTabAtribut.rbrAtrib

                AND tabAtribut.sifTablica  = dimCinj.sifDimTablica
                AND sifCinjTablica = %s
                AND tabAtribut.sifTipAtrib = 2
                ORDER BY dimTablica.nazTablica, rbrAtrib
                """ % curr_id
                
        (results, _) = execute_query(naredba, connection_string)
        for result in results:
            dim = result[0].strip()
            attr = result[1].strip()
            print(dim, attr)
            if dim not in tablice[tablica]['dimenzije']:
                tablice[tablica]['dimenzije'][dim] = {attr: False}
            else:
                tablice[tablica]['dimenzije'][dim][attr] = False
                
    pprint(tablice)
        
    
    
  

def run_query():
    global option, limit, use_limit, code_block, data
    
    limit_select = "SELECT TOP %d" % (limit) if use_limit else "SELECT"
    from_statement = "\nFROM %s" % (option)
    select = ""
    where = ""
    group_by = ""
    
    if option in tablice and 'mjere' in tablice[option]:
        for mjera in tablice[option]['mjere']:
            print(tablice[option]['mjere'][mjera])
            if tablice[option]['mjere'][mjera]['active']:
                select += '\n%s  as "%s",' % (tablice[option]['mjere'][mjera]['naredba'] , mjera)
            
    
    
    if option in tablice and 'dimenzije' in tablice[option]:
        for dim in tablice[option]['dimenzije']:
            present = False
            for attr in tablice[option]['dimenzije'][dim]:
                if tablice[option]['dimenzije'][dim][attr]:
                    present = True
                    if where == "":
                        where = "\nWHERE %s.%s = %s.%s" % (option, attr, dim, attr)
                    else: 
                        where += "\nAND %s.%s = %s.%s" % (option, attr, dim, attr)
                    select += '\n%s.%s as "%s_%s",' % (dim, attr, dim, attr)
                    group_by += '\n%s.%s,' % (dim, attr)
            if present:
                from_statement += "\n, %s" % (dim)
                
                
    
    if(group_by):
        group_by = group_by[:-1]
        group_by = "\nGROUP BY %s" % (group_by)


    
    if select == "":
        select = "\n*"
    
    if select[-1] == ",":
        select = select[:-1]

    code = """%s %s %s %s %s""" % (limit_select, select, from_statement, where, group_by)
  
    
    results, columns = execute_query(code, connection_string)
    data = pd.DataFrame(results, columns=columns)
    code_block = st.code(code, language='sql')
    st.subheader('Rezultat')
    st.write(data)
  
  
      
        

    
    
    
    
  

data_load_state = st.text('')


get_cinjenicne_tablice()

conn_string_from = st.sidebar.form(key="conn_string_from")

with conn_string_from:
    connection_string = st.text_input("connection string", value=SQL_SERVER_CONNECTION_STRING, max_chars=None, key=None, type="default", help=None, autocomplete=None, args=None, kwargs=None,  placeholder=None, disabled=False)   
    submitted = st.form_submit_button(label="Osvje??i")
    
if submitted:
    get_cinjenicne_tablice()




option = st.sidebar.selectbox("odaberite cinjenicnu tablicu", options=[opt.strip() for opt in cinjenicne_tablice])


form = st.sidebar.form(key="forma")

with form:

    with st.expander("Mjere"):
        if option in tablice and 'mjere' in tablice[option]:
            for mjera in tablice[option]['mjere']:
                tablice[option]['mjere'][mjera]['active'] = st.checkbox(mjera)

            

    with st.expander("Dimenzije"):
        if option in tablice and 'dimenzije' in tablice[option]:
            for k in tablice[option]['dimenzije'].keys():
                st.write(k)
                try:
                    for k2 in tablice[option]['dimenzije'][k].keys():
                        tablice[option]['dimenzije'][k][k2] = st.checkbox(k2)
                except:
                    st.write("vise atributa ima isto ime")
                    




    use_limit = st.checkbox("koristi limitator", value=True)
    limit = st.slider('limit', 0, 100, 10)


    query_ready = st.form_submit_button(label="Pokreni")
    
if query_ready:
    run_query()