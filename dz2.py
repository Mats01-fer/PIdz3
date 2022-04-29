
import pymssql


server = "localhost"
user = "sa"
password = "Strong.Pwd-123"

conn = pymssql.connect(server, user, password, "dz03")






naredba = """SELECT * from agrFun af;"""

cursor = conn.cursor()

cursor.execute(naredba)

row = cursor.fetchone()
while row:
    print("jedan=%d, dva=%s" % (row[0], row[1]))
    row = cursor.fetchone()


cursor.close()




# conn.commit()

conn.close()
