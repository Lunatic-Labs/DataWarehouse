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

curr.execute('SELECT * FROM "group";' )

data = curr.fetchall()

for row in data:
    print(row)

conn.close()

# if conn:
#     print("Connection to the PostgreSQL established successfully.")
# else:
#     print("Connection to the PostgreSQL encountered an error.")

# class checkTable:
#     def __init__(self, data):
#         self.data = data