import os
# import urllib       # This is most likely not needed, but idk.
# import urlparse     # This is most likely not needed, but idk.
# import urllib.parse # This is most likely not needed, but idk.
import pycurl
from io import BytesIO
import certifi

# Pycurl Documentation: http://pycurl.io/docs/latest/quickstart.html

class DWInterface:
    remote_ip_address = "44.204.92.26"
    local_ip_address = "127.0.0.1"

    development_port = 5000
    staging_port = 4000
    production_port = 3000

    def __init__(self, username, password, ip=local_ip_address, port=development_port, group_uuid=None, source_uuid=None, metric_uuid=None):
        self.__username = username
        self.__password = password
        self.__ip = ip
        self.__port = port
        self.__group_uuid = group_uuid
        self.__source_uuid = source_uuid
        self.__metric_uuid = metric_uuid

    # Private Functions.

    def __POSTRequest(self, url, json_file):
        '''
        This function should not return anything.
        '''
        pass

    def __GETRequest(self, url):
        '''
        This function should return a string that is the response from the server.
        '''
        # Create a buffer to recieve data.

        buf = BytesIO()
        # Create CURL handle.
        curl_handle = pycurl.Curl()

        # Set CURL options.
        curl_handle.setopt(curl_handle.URL, url)
        curl_handle.setopt(curl_handle.WRITEDATA, buf)
        curl_handle.setopt(curl_handle.CAINFO, certifi.where())

        # Perform CURL and cleanup.
        curl_handle.perform()
        curl_handle.close()

        # Get the response from the buffer and decode.
        body = buf.getvalue()
        return body.decode('iso-8859-1') # TODO: Need to find out the encoding from server.

    # Public Functions.

    def commitHandshake(self, handshake_json):
        pass

    def insertData(self, insert_json):
        pass

    def queryData(self, query_string):
        pass

    def setUUIDs(self, group_uuid, source_uuid, metric_uuid):
        pass

if __name__ == "__main__": # Use this for running code, testing, debugging, etc.
    dw = DWInterface("usr", "pass")

