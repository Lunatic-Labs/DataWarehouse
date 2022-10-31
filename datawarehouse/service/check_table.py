from email import message
import json
import sqlalchemy
import psycopg2

def get_connection():
    try:
        return psycopg2.connect(
            database="test",
            user="postgres",
            password="pre",
            host="127.0.0.1",
            port=5432,
        )
    except:
        return False

conn = get_connection()

curr = conn.cursor()

curr.execute('SELECT * FROM "group";')

data = curr.fetchall()

# if conn:
#     print("Connection to the PostgreSQL established successfully.")
# else:
#     print("Connection to the PostgreSQL encountered an error.")

class checkTable:
    def __init__(self, json_message):
        self.json_message = json_message

    def checkColumns(self):
        check_group = self.verifyGroup()
        check_source = self.verifySource()
        check_metric = self.verifyMetric()


    def verifyGroup(self):
        pass

    def verifySource(self):
        pass

    def verifyMetric(self):
        pass


conn.close()