import pymssql
import re

def execute_query(naredba, connection_string):    
    global code_block, data
    re_result = re.search(r"Server=(.+);Database=(.+);User Id=(.+);Password=(.+);", connection_string)
    server = re_result.group(1)
    user = re_result.group(3)
    database = re_result.group(2)
    password = re_result.group(4)
    results = []
    columns = []
    try:
        conn = pymssql.connect(server, user, password, database)
        cursor = conn.cursor()
        cursor.execute(naredba)
        columns = [i[0] for i in cursor.description]
        row = cursor.fetchone()
        while row:
            results.append(row)
            row = cursor.fetchone()
        cursor.close()
        # conn.commit()
        conn.close()
    except Exception as e:
      pass
    
    return results, columns