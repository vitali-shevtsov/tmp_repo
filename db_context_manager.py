import mysql.connector

class UseDatabase:

    def __init__(self):
        self.configuration =  {'host': '192.168.1.1',
                               'user': 'root',
                               'password': 'root',
                               'database': 'db1'}

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        self.cursor.execute("SET NAMES utf8;")
        self.cursor.execute("SET CHARACTER SET utf8;")
        self.cursor.execute("SET character_set_connection=utf8;")
        self.cursor.execute("USE db1;")
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
  
with UseDatabase() as cursor:
    cursor.execute("SELECT * FROM `table` WHERE 1")
    select = [x[0] for x in cursor.fetchall()]

    _SQL = ("""UPDATE table2 
               SET value1=%s,value2=%s 
               WHERE value3=%s 
	       AND value4=%s""")
    a,b,c,d = 1,2,3,4
    cursor.execute(_SQL, (a,b,c,d))
