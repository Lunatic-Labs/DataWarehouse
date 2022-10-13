import json
from typing import Optional

# with open("sample.json") as f:
#     data = json.load(f)


data = {
    "classification": "testing",
    "group_name": "Porter-Mckinney",
    "sources": [
        {
            "metrics": [
                {
                    "asc": False,
                    "data_type": "integer",
                    "name": "WeueKSwmjcGsYVThpwuf",
                    "units": "students",
                }
            ],
            "name": "Spedometer",
        }
    ],
}


class checkJsonFile:
    def __init__(self, data):
        self.data = data

    # Loops through the keys in the dictionaries
    def check_dict_keys(self):
        found_req = True
        found_opt = True

        val = None
        layer = None

        # Outer Layer
        for key in data.keys():
            layer = "outer"
            check_req = self.required_fields(key, layer)
            check_opt = self.optional_fields(key, layer)
            # print(check_opt)

            if not check_req:
                if not check_opt:
                    found_req = False
                    found_opt = False
                    val = key
                    break
                else:
                    found_opt = True
                    val = key
                    break

        # source Layer
        if found_req:
            for i in data["sources"]:
                for key in i.keys():
                    # print(key)
                    layer = "source"
                    check_req = self.required_fields(key, layer)
                    check_opt = self.optional_fields(key, layer)

                    if not check_req:
                        if not check_opt:
                            found_req = False
                            found_opt = False
                            val = key
                            break
                        else:
                            found_opt = True
                            val = key
                            break

        # Metric Layer
        if found_req:
            for i in data["sources"]:
                for j in i["metrics"]:
                    for key in j.keys():
                        layer = "metric"
                        check_req = self.required_fields(key, layer)
                        check_opt = self.optional_fields(key, layer)

                        if not check_req:
                            if not check_opt:
                                found_req = False
                                found_opt = False
                                val = key
                                break
                            else:
                                found_opt = True
                                val = key
                                break

        if not found_req and found_opt:
            print("Missing required field:", val)
        elif not found_opt or not found_req:
            print("Not a supported key", val)

    # Checks to see if all the required fields are provided in the JSON file
    def required_fields(self, val, layer):
        req_outer_layer = ["group_name", "sources"]
        req_source_layer = ["metrics", "name"]
        req_metric_layer = ["data_type", "name"]

        found = False

        if layer == "outer":
            for i in req_outer_layer:
                if val in i:
                    found = True

        if layer == "source":
            for i in req_source_layer:
                if val in i:
                    found = True

        if layer == "metric":
            for i in req_metric_layer:
                if val in i:
                    found = True

        return found

    # Checks all the accepted optional fields
    def optional_fields(self, val, layer):
        # print("checking: {}".format(val))
        opt_outer_layer = ["classification", "location"]
        opt_source_layer = ["tz_info"]
        opt_metric_layer = ["asc", "units"]

        found = False

        if layer == "outer":
            for i in opt_outer_layer:
                if val in i:
                    found = True

        if layer == "source":
            for i in opt_source_layer:
                if val in i:
                    found = True

        if layer == "metric":
            for i in opt_metric_layer:
                if val in i:
                    found = True

        return found


checker = checkJsonFile(data)
checker.check_dict_keys()

# check all the keys and see if it belongs in the table
# check if it is optional if it is not in the required

# optional


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
