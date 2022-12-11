import json
from typing import Optional

# Would use if opening a JSON file
with open("sample.json") as f:
    data = json.load(f)


class checkJsonFile:
    def __init__(self, data):
        self.data = data

    # Loops through the keys in the dictionaries
    def checkDictKeys(self):
        check_outer = self.verifyOuter()
        check_source = self.verifySources()
        check_metric = self.verfiyMetrics()
        check_required = self.verifyRequired()

        if (
            not check_outer
            or not check_source
            or not check_metric
            or not check_required
        ):
            return False
        return True

    # Checks the outer layer dictionary
    def verifyOuter(self):
        correct = None
        layer = 1

        for outer in self.data.keys():
            check_req = self.requiredFields(outer, layer)
            check_opt = self.optionalFields(outer, layer)
            correct = self.supportedType(check_req, check_opt)

        return correct

    # Checks the sources layer dictionary
    def verifySources(self):
        correct = None
        layer = 2

        for source in self.data["sources"]:
            for key in source.keys():
                check_req = self.requiredFields(key, layer)
                check_opt = self.optionalFields(key, layer)
                correct = self.supportedType(check_req, check_opt)

        return correct

    # Checks the metrics layer dictionary
    def verfiyMetrics(self):
        correct = None
        layer = 3

        for source in self.data["sources"]:
            for metric in source["metrics"]:
                for key in metric.keys():
                    check_req = self.requiredFields(key, layer)
                    check_opt = self.optionalFields(key, layer)
                    correct = self.supportedType(check_req, check_opt)

        return correct

    # Returns the result of whether the key is a supported value
    def supportedType(self, check_req, check_opt):
        if not check_opt:
            if not check_req:
                return False
        return True

    # Checks to see if all the required fields are provided
    def verifyRequired(self):
        req_outer_layer = ["group_name", "sources"]
        req_source_layer = ["metrics", "name"]
        req_metric_layer = ["data_type", "name"]

        # Checks the outer layer dictionary
        for val in req_outer_layer:
            if not val in data:
                print("Missing required field:", val)
                return False

        # Checks the sources layer dictionary
        for val in req_source_layer:
            for source in data["sources"]:
                if not val in source:
                    print("Missing required field:", val)
                    return False

        # Checks the metrics layer dictionary
        for val in req_metric_layer:
            for source in data["sources"]:
                for metric in source["metrics"]:
                    if not val in metric:
                        print("Missing required field:", val)
                        return False

        return True

    # Checks to see if the val is one of the required fields
    def requiredFields(self, val, layer):
        req_outer_layer = ["group_name", "sources"]
        req_source_layer = ["metrics", "name"]
        req_metric_layer = ["data_type", "name"]

        found = False

        # Outer layer
        if layer == 1:
            for key in req_outer_layer:
                if val == key:
                    found = True

        # Source layer
        if layer == 2:
            for key in req_source_layer:
                if val == key:
                    found = True

        # Metric layer
        if layer == 3:
            for key in req_metric_layer:
                if val == key:
                    found = True

        return found

    # Checks to see if the val is one of the optional fields
    def optionalFields(self, val, layer):
        opt_outer_layer = ["classification", "location"]
        opt_source_layer = ["tz_info"]
        opt_metric_layer = ["asc", "units"]

        found = False

        # Outer layer
        if layer == 1:
            for key in opt_outer_layer:
                if val == key:
                    found = True

        # Source layer
        if layer == 2:
            for key in opt_source_layer:
                if val == key:
                    found = True

        # Metric layer
        if layer == 3:
            for key in opt_metric_layer:
                if val == key:
                    found = True

        return found


checker = checkJsonFile(data)
print(checker.checkDictKeys())


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
