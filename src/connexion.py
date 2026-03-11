import os
import mysql.connector
from mysql.connector import errorcode, pooling
class ConnexionSql:
    pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host= os.getenv("MYSQL_HOST"),
    user= os.getenv("MYSQL_USER"),
    database= os.getenv("MYSQL_DB"),password=os.getenv("MYSQL_PASSWORD"),
    database= os.getenv("MYSQL_DB")
)

    # En cada request:
    cnnx = pool.get_connection()

    try:
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

    def lookForUser(self,numberClient,cnnx):
        sql = "SELECT 1 FROM Clients WHERE phoneNumber = %s LIMIT 1"
        with cnnx.cursor() as cur:
            cur.execute(sql, (numberClient,))
            result = cur.fetchone()   # consumir aquí
        return result is not None
    
    def already_processed(self,idMessage, cnnx):
        sql= "SELECT 1 FROM processed_messages WHERE id_message = %s"
        with cnnx.cursor() as cur:
             cur.execute(sql, (idMessage,))
             return cur.fetchone() is not None

    def mark_processed(self,idMessage, cnnx):
        sql = "INSERT INTO processed_messages (id_message) VALUES (%s)"
        with cnnx.cursor() as cur:
             cur.execute(sql, (idMessage,))
             cnnx.commit()

       
