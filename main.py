import json

class CreateHandshake:
    def __init__(self, class_, name):
        self.dict_object = {"classification": class_, "group_name": name, "sources": []}

    def insert_metric_into_source(self, asc, dt, name, units):
        self.dict_object["sources"][len(self.dict_object['sources']) - 1]["metrics"].append({"asc": asc, "dt": dt, "name": name, "units": units})

    def insert_source_into_group(self, name):
        self.dict_object["sources"].append({"name": name, "metrics": []})

def create_handshake():
    handshake = CreateHandshake("Academia", "Lunatic Labs University")
    handshake.insert_source_into_group("Python Class Stats")
    handshake.insert_metric_into_source(False, "5", "students_present_asdf", "students_asdf")
    handshake.insert_source_into_group("Python Class Stats 2")
    handshake.insert_metric_into_source(False, "4", "students_present", "students")
    
    group = json.dumps(handshake.dict_object, indent=4)
    print(group)

create_handshake()