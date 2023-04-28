import json

'''
This class creates a handshake JSON file in the below format: 
{
    "classification": "Academia",
    "group_name": "Lunatic Labs University",
    "sources": [
        {
            "name": "Python Class Stats",
            "metrics": [
                {
                    "asc": false,
                    "dt": "5",
                    "name": "students_present_asdf",
                    "units": "students_asdf"
                }
            ]
        },
        {
            "name": "Python Class Stats 2",
            "metrics": [
                {
                    "asc": false,
                    "dt": "4",
                    "name": "students_present",
                    "units": "students"
                }
            ]
        }
    ]
}

The JSON object that is output is received by the handshake protocol, where the UUIDs are 
added to the object
'''

class CreateHandshake:
    def __init__(self, class_, name):
        self.source_list = []
        self.dict_object = {"classification": class_, "group_name": name, "sources": []}

    def append_source_into_group(self, name):        
        self.source_list.append(0)
        self.dict_object["sources"].append({"name": name, "metrics": []})

    def append_metric_into_last_source(self, asc, dt, name, units):
        # Assert that there is a data source to add the metric into. 
        assert len(self.source_list) > 0, \
            "You must call the append_source_into_group function first to define your first data source."

        self.source_list[len(self.source_list) - 1] += 1
        self.dict_object["sources"][len(self.dict_object['sources']) - 1]["metrics"].append(
            {"asc": asc, "dt": dt, "name": name, "units": units}
        )

    def convert_to_json(self):
        # Assert that there is at least one source defined. 
        assert len(self.source_list) > 0, "You must define at least one data source."

        # Assert that each data source has at least one metric defined. 
        for i in range(len(self.source_list)):
            assert self.source_list[i] > 0, f"You must define at least one metric for data source #{i + 1}."

        # Otherwise, everything is all good. 
        final_output = json.dumps(self.dict_object, indent=4)
        print(final_output)

if __name__ == "__main__":
    # Create the outermost layer of the onion.
    # The CreateHandshake function must always be called first. 
    handshake = CreateHandshake("Academia", "Lunatic Labs University")

    # Add source #1
    handshake.append_source_into_group("Python Class Stats")

    # Add metric #1 inside of source #1
    handshake.append_metric_into_last_source(False, "5", "students_present_asdf", "students_asdf")

    # Add source #2
    handshake.append_source_into_group("Python Class Stats 2")

    # Add metric #1 inside of source #2
    handshake.append_metric_into_last_source(False, "4", "students_present", "students")

    # Convert to JSON object
    handshake.convert_to_json()