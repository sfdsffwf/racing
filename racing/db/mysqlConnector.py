import mysql.connector

class MysqlConnector():
    def __init__(self):
        self.mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="666666",
            database="racing")

    def batch_insert_sql(self,sql,val):
        mycursor = self.mydb.cursor()
        mycursor.executemany(sql, val)
        self.mydb.commit()
        print(mycursor.rowcount, "was inserted.")

    def select_sql(self,sql):
        mycursor = self.mydb.cursor()
        mycursor.execute(sql)
        return mycursor.fetchall()
