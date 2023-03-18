import os
# import urllib       # This is most likely not needed, but idk.
# import urlparse     # This is most likely not needed, but idk.
# import urllib.parse # This is most likely not needed, but idk.
import pycurl
from io import BytesIO
import certifi
import uuid

# Pycurl Documentation: http://pycurl.io/docs/latest/quickstart.html

class DWInterface:
    remote_ip_address = '3.216.190.202'
    local_ip_address = '127.0.0.1'

    handshake_path = '/api/prepare/'
    insert_path = '/api/store/'
    query_path = '/api/query/'

    development_port = ':5000'
    staging_port = ':4000'
    production_port = ':3000'

    def __init__(self, username, password, ip=local_ip_address, port=development_port, group_uuid=None, source_uuid=None, metric_uuid=None):
        self.__username = username
        self.__password = password
        self.__ip = ip
        self.__port = port
        self.__group_uuid = group_uuid
        self.__source_uuid = source_uuid
        self.__metric_uuid = metric_uuid
        self.__authority = 'http://' + ip + port
        self.__handshake_url = self.__authority + self.handshake_path
        self.__insert_url = self.__authority + self.insert_path
        self.__query_url = self.__authority + self.query_path
        self.__curl_handle = pycurl.Curl()

    # Private Functions.

    def __POSTRequest(self, url, json_filepath, out_filepath):
        '''
        This function should not return anything.
        curl_handle.setopt(pycurl.HTTPPOST, [('fileupload', (pycurl.FORM_FILE, json_file)), ('string', 'string_value')])
        '''
        outfp = None

        # Open the file if it is specified.
        if (out_filepath != None):
            outfp = open(out_filepath, "w")

        # Create a buffer to recieve data.
        buf = BytesIO()

        # Create CURL handle.
        self.__curl_handle = pycurl.Curl()
        self.__curl_handle.setopt(self.__curl_handle.URL, url)
        self.__curl_handle.setopt(self.__curl_handle.HTTPPOST, [('fileupload', (self.__curl_handle.FORM_FILE, json_filepath))])
        self.__curl_handle.perform()
        self.__curl_handle.close()

        # Get the response from the buffer and decode.
        body = buf.getvalue()
        response = body.decode('iso-8859-1')

        # Write to a file if an outfile is specified.
        if (out_filepath != None):
            outfp.write(response)

        return response

    def __GETRequest(self, query_string, out_filepath):
        '''
        This function should return a string that is the response from the server.
        '''
        outfp = None

        # Check to make sure the UUIDs have been set.
        if (self.__group_uuid is None or self.__source_uuid is None or self.__metric_uuid is None):
            raise ValueError('UUIDs must be set')

        if (query_string[0] != '?'):
            raise ValueError('Query string must start with `?`')

        # Open the file if it is specified.
        if (out_filepath != None):
            outfp = open(out_filepath, "w")

        # Create the url. It should be: 'http://ip_addr:port/group_uuid/source_uuid/query_string
        url = self.__query_url + self.__group_uuid + '/' + self.__source_uuid + '/' + query_string

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
        response = body.decode('iso-8859-1')

        # Write to a file if an outfile is specified.
        if (out_filepath != None):
            outfp.write(response)

        return response

    def __verifyUUID(self, unverified_uuid):
        try:
            uuid.UUID(str(unverified_uuid))
            return True
        except ValueError:
            return False;

    # Public Functions.

    def commitHandshake(self, handshake_json):
        pass

    def insertData(self, insert_json):
        pass

    def queryData(self, query_string, out_file=None):
        return self.__GETRequest(query_string, out_file)

    def setUUIDs(self, group_uuid, source_uuid, metric_uuid):
        if self.__verifyUUID(group_uuid) and self.__verifyUUID(source_uuid) and self.__verifyUUID(metric_uuid):
            self.__group_uuid = group_uuid
            self.__source_uuid = source_uuid
            self.__metric_uuid = metric_uuid
        else:
            raise ValueError('Invalid UUIDs provided')

if __name__ == '__main__': # Use this for running code, testing, debugging, etc.
    guuid = 'c85ad1d4-2147-44eb-ba30-3206f26d6569'
    suuid = '3d276782-6656-4e5e-b41c-6236ac86a021'
    muuid = '75b9d8f7-9e39-47b5-909a-76d0e2c9cb13'

    dw = DWInterface('usr', 'pass')
    dw.setUUIDs(guuid, suuid, muuid)

# Good job with this, it'll be useful.
#post_request() is called within commit_handshake() and insert_data().
#This seems to be where the gruntwork of POSTing using PycURL happens.
# post_request(dwi, url, json_file)
# {
#     c = pycurl.Curl()
#     c.setopt(c.URL, url)

#     #Set the content type header to application/json.
#     c.setopt(c.HTTPPOST, [
#     ('fileupload', (
#         c.FORM_BUFFER, json_file,
#         c.FORM_CONTENTTYPE, 'Content-Type: application/json',
#     )),
#     ])

#     #Get the file data and set the request body to these contents.
#     try
#         file_data = open(json_file, 'r')
#     except IOError
#         PANIC('Post_request() failed to read file contents')
#         exit(1)
#     c.setopt(c.POSTFIELDS, urlencode(file_data.read()))    #data must be urlencoded for PycURL

#     #get the size of the file and set the request body size to match.
#     json_file.seek(0, os.SEEK_END)
#     file_size = json_file.tell()
#     c.setopt(c.POSTFIELDSIZE, file_size)

#     c.perform()
#     c.close()
#     file_data.close()

#     #NEED TO: assign and return a response? What is it, and why are we returning it?
# }
