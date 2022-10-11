import json

with open("sample.json") as f:
    data = json.load(f)


class checkJsonFile:
    def __init__(self, data):
        self.data = data

    @classmethod
    def check_dictionaries(self, val):
        for i in data["sources"]:
            print(i.values())
        #     if val in i:
        #         return True
        # return False

    @classmethod
    def required_fields(self):
        req_outer_layer = ["group_name", "sources"]
        req_source_layer = ["metrics", "name"]
        req_metric_layer = ["data_type", "name"]

        for i in req_outer_layer:
            if i not in data:
                print("Missing required field:", i)

        for i in req_source_layer:
            if not self.check_dictionaries(i):
                print("Missing required field:", i)

        # for i in req_metric_layer:
        #     if not self.check_dictionaries(i):
        #         print("Missing required field:", i)


# d = checkJsonFile(data)
# print(d.data)

checker = checkJsonFile(data)
checker.required_fields()


# Outermost Layer
# group_name    string      required        Title of the group
# sources       string      optional        Type of the data taken in
# location      string      optional        Where the data is sourced from
# sources       array       required        an array of sources (Json object)

# Source Layer
# metrics       array       required        an array of metrics (Json object)
# name          string      required        the name of the source
# tz.info       string      optional        timezone

# Metric Layer
# asc           boolean     optional        Default sort direction
# data_type     string      REQUIRED        MUST BE A SUPPORTED DATA_TYPE
# name          string      required        name of the metric (column)
# units         string      optional        units of measurement
