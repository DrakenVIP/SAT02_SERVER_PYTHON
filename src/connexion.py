import os
import mysql.connector
from mysql.connector import errorcode
class ConnexionSql:
    try:
        global cnnx
        cnnx = mysql.connector.connect(user= os.getenv("MYSQL_USER"),host= os.getenv("MYSQL_HOST"),database= os.getenv("MYSQL_DB"),password=os.getenv("MYSQL_PASSWORD"))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    else:
        print('Good connecting')

    def lookForUser(self,numberClient):
        sql = "SELECT 1 FROM Clients WHERE phoneNumber = %s LIMIT 1"
        with cnnx.cursor() as cur:
            cur.execute(sql, (numberClient,))
            result = cur.fetchone()   # consumir aquí
        return result is not None
       
