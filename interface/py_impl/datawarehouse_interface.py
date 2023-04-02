import os

# import urllib       # This is most likely not needed, but idk.
# import urlparse     # This is most likely not needed, but idk.
# import urllib.parse # This is most likely not needed, but idk.
import pycurl
from io import BytesIO
import certifi
import uuid
import json

# Pycurl Documentation: http://pycurl.io/docs/latest/quickstart.html

#Define the Data Warehouse data hierarchy: DWInterface > Groups > Sources > Metrics
class Metric:
    def __init__(
        self,
        asc,
        datatype,
        name,
        units
    ):
        self.asc = asc
        self.datatype = datatype
        self.name = name
        self.units = units

class Source:
    def __init__(
        self,
        name,
        metric=None
    ):
        self.name = name
        self.metrics = list(metric)

class Group:
    def  __init__(
        self,
        classification,
        name,
        source=None
    ):
        self.classification = classification
        self.name = name
        self.sources = list(source)

class DWInterface:
    remote_ip_address = "3.216.190.202"
    local_ip_address = "127.0.0.1"

    handshake_path = "/api/prepare/"
    insert_path = "/api/store/"
    query_path = "/api/query/"

    development_port = ":5000"
    staging_port = ":4000"
    production_port = ":3000"

    def __init__(
        self,
        username,
        password,
        ip=local_ip_address,
        port=development_port,
        group_uuid=None,
        source_uuid=None,
        metric_uuid=None
    ):
        
        self.__username = username
        self.__password = password
        self.__ip = ip
        self.__port = port
        self.__group_uuid = group_uuid
        self.__source_uuid = source_uuid
        self.__metric_uuid = metric_uuid
        self.__authority = "http://" + ip + port
        self.__handshake_url = self.__authority + self.handshake_path
        self.__insert_url = self.__authority + self.insert_path
        self.__query_url = self.__authority + self.query_path
        self.__curl_handle = pycurl.Curl()
        self.groups = list()

    # Private Functions.

    def __POSTRequest(self, json_filepath, out_filepath):
        """
        This function should return the data from commitHandshake()
        as there is no need to return anything from insertData().
        """
        outfp = None
        json_file = None
        with open(json_filepath) as f:
            json_file = json.load(f)

        print(json.dumps(json_file))

        # Open the file if it is specified.
        if out_filepath != None:
            outfp = open(out_filepath, "w")

        # Create a buffer to recieve data.
        buf = BytesIO()

        self.__curl_handle.setopt(self.__curl_handle.URL, self.__handshake_url)
        self.__curl_handle.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
        self.__curl_handle.setopt(self.__curl_handle.POSTFIELDS, json.dumps(json_file))
        self.__curl_handle.setopt(self.__curl_handle.WRITEFUNCTION, lambda x: None)

        # Perform the CURL, returning a response string.
        response = self.__curl_handle.perform_rs()
        self.__curl_handle.close()

        # Write to a file if an outfile is specified.
        if out_filepath != None:
            outfp.write(response)

        return response

    def __GETRequest(self, query_string, out_filepath):
        """
        This function should return a string that is the response from the server.
        """
        outfp = None

        # Check to make sure the UUIDs have been set.
        if (
            self.__group_uuid is None
            or self.__source_uuid is None
            or self.__metric_uuid is None
        ):
            raise ValueError("UUIDs must be set")

        if query_string[0] != "?":
            raise ValueError("Query string must start with `?`")

        # Open the file if it is specified.
        if out_filepath != None:
            outfp = open(out_filepath, "w")

        # Create the url. It should be: 'http://ip_addr:port/group_uuid/source_uuid/query_string
        url = (
            self.__query_url
            + self.__group_uuid
            + "/"
            + self.__source_uuid
            + "/"
            + query_string
        )

        # Create a buffer to recieve data.
        buf = BytesIO()

        # Set CURL options.
        self.__curl_handle.setopt(self.__curl_handle.URL, url)
        self.__curl_handle.setopt(self.__curl_handle.WRITEDATA, buf)
        self.__curl_handle.setopt(self.__curl_handle.CAINFO, certifi.where())
        self.__curl_handle.setopt(pycurl.HTTPGET, 1)

        # Perform CURL and cleanup.
        self.__curl_handle.perform()
        self.__curl_handle.close()

        # Get the response from the buffer and decode.
        body = buf.getvalue()
        response = body.decode("iso-8859-1")

        # Write to a file if an outfile is specified.
        if out_filepath != None:
            outfp.write(response)

        return response

    def __verifyUUID(self, unverified_uuid):
        try:
            uuid.UUID(str(unverified_uuid))
            return True
        except ValueError:
            return False

    # Public Functions.

    def commitHandshake(self, handshake_json, out_file_path=None):
        return self.__POSTRequest(handshake_json, out_file_path)

    def insertData(self, insert_json):
        self.__POSTRequest(insert_json, None)

    def queryData(self, query_string, out_file=None):
        return self.__GETRequest(query_string, out_file)

    def setUUIDs(self, group_uuid, source_uuid, metric_uuid):
        if (
            self.__verifyUUID(group_uuid)
            and self.__verifyUUID(source_uuid)
            and self.__verifyUUID(metric_uuid)
        ):
            self.__group_uuid = group_uuid
            self.__source_uuid = source_uuid
            self.__metric_uuid = metric_uuid
        else:
            raise ValueError("Invalid UUIDs provided")
        
    def dwInterfaceGroupCreate(self, classification, name):
        self.groups.append(Group(classification, name))

    def dwInterfaceSourceCreate(self, group, name):
        group.sources.append(Source(name))

    def dwInterfaceMetricCreate(self, source, name, units):
        source.metrics.append(Metric(name, units))

    def checkLength(self, thing):       #Returns the length of of a DWInterface, Group, or Source 
        if (type(thing) == DWInterface):
            return len(thing.groups)
        elif (type(thing) == Group):
            return len(thing.sources)
        elif (type(thing) == Source):
            return len(thing.metrics)
        else
            return


if __name__ == "__main__":  # Use this for running code, testing, debugging, etc.
    guuid = "2632e2c8-a9ef-4c59-b555-edf5d5a51dfe"
    suuid = "99113101-f382-4c1f-a687-96479237cac8"
    muuid = "f909dddb-15c1-466a-88f2-7975fa494f65"

    dw = DWInterface("usr", "pass")
    # dw.commitHandshake("../../../handshake.json", "handshake.out")
    dw.setUUIDs(guuid, suuid, muuid)
    #dw.insertData("../../../insert.json")
    dw.insertData("insert.json")



