from email import message
import json
import sqlalchemy
import psycopg2

with open("sample.json") as f:
    json_file = json.load(f)

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

class checkTable:
    def __init__(self, json_message):
        self.json_message = json_message


    def checkColumns(self):
        check_group = self.verifyGroup()
        check_source = self.verifySource()
        check_metric = self.verifyMetric()


    def verifyGroup(self):
        curr.execute('SELECT * FROM "group";')
        data = curr.fetchall()

        for val in self.json_message.values():
            print(val)

        # for row in data:
        #     for val in row:
        #         print(val)
        

    def verifySource(self):
        curr.execute('SELECT * FROM "source";')
        data = curr.fetchall()
        
        for row in self.json_message["sources"]:
            for val in row.values():
                print(val)
        
        # for row in data:
        #     for val in row:
        #         print(val)
    

    def verifyMetric(self):
        curr.execute('SELECT * FROM "metric";')
        data = curr.fetchall()
        
        for source in self.json_message["sources"]:
            for metric in source["metrics"]:
                for val in metric.values():
                    print(val)

        # for row in data:
        #     for val in row:
        #         print(val)


checker = checkTable(json_file)
print(checker.checkColumns())

curr.close()
conn.close()