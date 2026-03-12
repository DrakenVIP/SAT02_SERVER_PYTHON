import os
import mysql.connector
from mysql.connector import errorcode, pooling
class ConnexionSql:
    pool = pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    host= os.getenv("MYSQL_HOST"),
    user= os.getenv("MYSQL_USER"),
    database= os.getenv("MYSQL_DB"),
    password=os.getenv("MYSQL_PASSWORD")
)
    def __init__(self):
        try:
            cnnx = ConnexionSql.pool.get_connection()
            print("Conexión exitosa")
            cnnx.close()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Usuario o contraseña incorrectos")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("La base de datos no existe")
            else:
                print(err)


    def lookForUser(self, numberClient):
        cnnx = ConnexionSql.pool.get_connection()
        with cnnx.cursor() as cur:
            sql = "SELECT 1 FROM Clients WHERE phoneNumber = %s LIMIT 1"
            cur.execute(sql, (numberClient,))
            result = cur.fetchone()
            cur.close()
        cnnx.close()
        return result is not None
    
    def register_user(self,fullName,idCard,phoneNumber):
        cnnx = ConnexionSql.pool.get_connection()
        with cnnx.cursor() as cur:
            sql = "INSERT INTO Clients (fullName,idCard,phoneNumber) VALUES (%s, %s, %s)"
            cur.execute(sql, (fullName,idCard,phoneNumber))
            cnnx.commit()
        cnnx.close()
        

    
    def already_processed(self, idMessage):
        cnnx = ConnexionSql.pool.get_connection()
        with cnnx.cursor() as cur:
            sql = "SELECT 1 FROM processed_messages WHERE id_message = %s"
            cur.execute(sql, (idMessage,))
            result = cur.fetchone()
            return result is not None
        cnnx.close()
        

    def mark_processed(self, idMessage):
        cnnx = ConnexionSql.pool.get_connection()
        with cnnx.cursor() as cur:
            sql = "INSERT INTO processed_messages (id_message) VALUES (%s)"
            cur.execute(sql, (idMessage,))
            cnnx.commit()
        cnnx.close()
    
    

       
