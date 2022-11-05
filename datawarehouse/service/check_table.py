from email import message
import json
import sqlalchemy
import psycopg2

with open("sample.json") as f:
    json_file = json.load(f)

conn = psycopg2.connect(
    database="test", user='postgres', password='pre', host="127.0.0.1", port='5432'
)
curr = conn.cursor()

class checkTable:
    def __init__(self, json_message):
        self.json_message = json_message


    def checkColumns(self):
        check_group = self.verifyGroup()
        check_source = self.verifySource()
        check_metric = self.verifyMetric()

        if(
            not check_group 
            or not check_source
            or not check_metric
        ):
            return False
        return True


    def verifyGroup(self):
        curr.execute('SELECT * FROM "group";')
        data = curr.fetchall()

        for key, value in self.json_message.items():
            for row in data:
                if key == 'sources':
                    continue
                elif value not in row:
                    return False

        return True
        

    def verifySource(self):
        curr.execute('SELECT * FROM "source";')
        data = curr.fetchall()

        for source in self.json_message["sources"]:
            for key, value in source.items():
                for row in data:
                    if key == 'metrics':
                        continue
                    elif value not in row:
                        return False

        return True
    

    def verifyMetric(self):
        curr.execute('SELECT * FROM "metric";')
        data = curr.fetchall()
        
        for source in self.json_message["sources"]:
            for metric in source["metrics"]:
                for value in metric.values():
                    for row in data:
                        if value not in row:
                            return False
        
        return True



checker = checkTable(json_file)
print(checker.checkColumns())

curr.close()
conn.close()