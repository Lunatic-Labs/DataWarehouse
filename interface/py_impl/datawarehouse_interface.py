import os

# import urllib       # This is most likely not needed, but idk.
# import urlparse     # This is most likely not needed, but idk.
# import urllib.parse # This is most likely not needed, but idk.
import pycurl
from io import BytesIO
import certifi
import uuid
import json
import logging

# Pycurl Documentation: http://pycurl.io/docs/latest/quickstart.html

#Data hierarchy (DWI > G > S > M). 
# Unlike their first implementation, using solely to store names and UUIDs.
#These are used in the setVal() function later.
class Metric:
    def __init__(
        self,
        name,
        value=None,
        uuid=None
    ):
        self.name = name
        self.uuid = uuid
        self.value = value

class Source:
    def __init__(
        self,
        name,
        metric=None,
        uuid=None
    ):
        self.name = name
        self.metrics = list(metric)
        self.uuid = uuid

class Group:
    def  __init__(
        self,
        classification,
        name,
        source=None,
        uuid=None
    ):
        self.classification = classification
        self.name = name
        self.sources = list(source)
        self.uuid = uuid

class DWInterface:
    remote_ip_address = "3.216.190.202"
    local_ip_address = "127.0.0.1"

    handshake_path = "/api/prepare/"
    insert_path = "/api/store/"
    query_path = "/api/query/"

    interface_handshake_path = "/api/interface_prepare/"
    interface_insert_path = "/api/interface_store/"
    interface_query_path = "/api/interface_query/" 

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
        metric_uuid=None,
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
        self.__interface_handshake_url = self.__authority + self.interface_handshake_path
        self.__interface_insert_url = self.__authority + self.interface_insert_path
        self.__interface_query_url = self.__authority + self.interface_query_path
        self.__curl_handle = pycurl.Curl()
        self.groups = list()

    # Private Functions.

    def __POSTRequest(self, json_filepath, out_filepath, url):
        """
        This function should return the data from commitHandshake()
        as there is no need to return anything from insertData().
        """
        outfp = None
        json_file = None
        with open(json_filepath) as f:
            try:
                json_file = json.load(f)
            except Exception as Argument:
 
            # creating/opening a file
                error = open("pyErrorFile.txt", "a")

            # writing in the file
                error.write(str(Argument))

            # closing the file
                error.close()

        print(json.dumps(json_file))

        # Open the file if it is specified.
        if out_filepath != None:
            try: 
                outfp = open(out_filepath, "w")

            except Exception as Argument:
 
            # creating/opening a file
                error = open("pyErrorFile.txt", "a")

            # writing in the file
                error.write(str(Argument))

            # closing the file
                error.close()

        # Create a buffer to recieve data.
        buf = BytesIO()

        self.__curl_handle.setopt(self.__curl_handle.URL, url) #Should use interface_handshake_url?
        self.__curl_handle.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json'])
        self.__curl_handle.setopt(self.__curl_handle.POSTFIELDS, json.dumps(json_file))
        self.__curl_handle.setopt(self.__curl_handle.WRITEFUNCTION, lambda x: None)

        # Perform the CURL, returning a response string.
        response = self.__curl_handle.perform_rs()
        self.__curl_handle.close()

        # Write to a file if an outfile is specified.
        if out_filepath != None:
            try:
                outfp.write(response)

            except Exception as Argument:
 
            # creating/opening a file
                error = open("pyErrorFile.txt", "a")

            # writing in the file
                error.write(str(Argument))

            # closing the file
                error.close()

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
            try:
                outfp = open(out_filepath, "w")
            except Exception as Argument:
 
            # creating/opening a file
                error = open("pyErrorFile.txt", "a")

            # writing in the file
                error.write(str(Argument))

            # closing the file
                error.close()

        # Create the url. It should be: 'http://ip_addr:port/group_uuid/source_uuid/query_string
        url = (
            self.__query_url    #Should be interface_query_url?
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
            try:
                outfp.write(response)

            except Exception as Argument:
 
            # creating/opening a file
                error = open("pyErrorFile.txt", "a")

            # writing in the file
                error.write(str(Argument))

            # closing the file
                error.close()

        return response

    def __verifyUUID(self, unverified_uuid):
        try:
            uuid.UUID(str(unverified_uuid))
            return True
        except ValueError as Argument:
            
            # creating/opening a file
                error = open("pyErrorFile.txt", "a")

            # writing in the file
                error.write(str(Argument))

            # closing the file
                error.close()
            
        return False

    # Public Functions.

    def commitHandshake(self, handshake_json, out_file_path=None):
        return self.__POSTRequest(handshake_json, out_file_path, self.__handshake_url)

    def insertData(self, insert_json):
        self.__POSTRequest(insert_json, None, self.__insert_url)

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
            #Set each UUID in related Group, Source, and Metric classes too?
        else:
            raise ValueError("Invalid UUIDs provided")
    
    def jsonToString(self, source, metric, value, handshake_filepath):
        #Receive Group, Source, and Metric by plaintext name
        #guuid = None
        suuid = None
        muuid = None
        if (handshake_filepath == None):
            raise ValueError("Please pass a handshake filepath")
        #Find related UUIDs for both
        #Implementation v3: comb file line by line for names and find other info. based on current line number
        #handshake = json.loads(handshake_filepath)
        with open(handshake_filepath, "r") as file:
            lines = file.readlines()
            i = 0
            for row in lines:                           #.lower()'ing all strings as a safeguard
                # if group.lower() in row.lower():        #If name found, 
                #     temp = (loop-2).split(':')                 #GUUID should be 2 lines previous.
                #     guuid = temp[1].strip(",\"")
                #     temp = (loop-3).split(':')                 #Classification should be 3 lines previous.
                #     gclass = temp[1].strip(",\"")
                if source.lower() in row.lower():     #If name found,
                    temp = lines[i+1].split(':')                 #SUUID should be on next line.
                    suuid = temp[1].strip(",\"\n ")
                elif metric.lower() in row.lower():     #If name found, 
                    temp = lines[i-1].split(':')                 #MUUID should be on previous line.
                    muuid = temp[1].strip(",\"\n ")    
                    temp = lines[i-2].split(':')                 #datatype should be 2 lines previous.
                    mdata = temp[1].strip(",\"\n ")
                    temp = lines[i-3].split(':')                 #asc should be 3 lines previous.
                    masc = temp[1].strip(",\"\n ")    
                i += 1   

        #Write relevant data as string (":"-separated) and return 
        #Format: "groupuid`name`classification`sourceuid`name`metricuid`asc`name`datatype"
        #Format 4/17/2023: "groupuuid`sourceuuid`metricuuid`value"
        self.setUUIDs(guuid, suuid, muuid)
        #If this setUUIDs() call is inappropriate, revert to the below logic
        
        # if guuid == None:
        #     raise ValueError("Group not in provided handshake file")
        # elif suuid == None:
        #     raise ValueError("Source not in provided handshake file")
        # elif muuid == None:
        #     raise ValueError("Metric not in provided handshake file")
        #else:
        #return guuid + '`' + group + '`' + gclass + '`' + suuid + '`' + source + '`' + muuid + '`' + masc + '`' + metric + '`' + mdata
        return suuid + '`' + muuid + '`' + str(value)
    
if __name__ == "__main__":  # Use this for running code, testing, debugging, etc.
    guuid = "2632e2c8-a9ef-4c59-b555-edf5d5a51dfe"
    suuid = "99113101-f382-4c1f-a687-96479237cac8"
    muuid = "f909dddb-15c1-466a-88f2-7975fa494f65"

    dw = DWInterface("usr", "pass")
    # dw.commitHandshake("../../../handshake.json", "handshake.out")
    dw.setUUIDs(guuid, suuid, muuid)
    #dw.insertData("../../../insert.json")
    dw.insertData("insert.json")
    #Below: Example call to jsonToString()
    print(dw.jsonToString("Python Class Stats", "students_present", 50, "handshake.out"))


