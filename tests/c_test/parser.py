import json

with open('insert.json', 'r') as out_file:
    data = json.load(out_file)

class getUUIDs:
    def __init__(self, data):
        self.data = data
    
    def getGUUID(self):
        pass

    def getSUUID(self):
        return data["source_uid"]
            
    def getMUUID(self):
        for metric in data["metrics"]:
            return metric["metric_uid"]


