from DataWarehouse.datawarehouse.service import data_insert_service
from uuid import uuid4 # will allow us to creat uuids
import os
import pycurl
import sys

# REMOTE_IP_ADDR      = "54.159.108.136"
# LOCAL_IP_ADDR       = "127.0.0.1"

# DEVELOPMENT_PORT    = 5000
# STAGING_PORT        = 4000
# PRODUCTION_PORT     = 3000

class DWInterface():
    # Not sure param names yet
    def __init__(self, data, json):
        self.data = data
        self.json = json

    def queryData(self):
        pass

    def insertData(self):
        pass
    
    def commitHandshake(self):
        # Possible way to verify uuid's exist
        if not data_insert_service.InsertDataService.verifyInformation(self.data):
            return "DWInterface uuids must be set"

  
#LINE: Stand-in for the C Macro that's used in that interface. This returns the current line number, for debug purposes. 
def LINE():
    return sys._getframe(1).f_lineno

#PANIC: A macro that prints an error message and exits the program with a
  #failure status. It takes a message as an argument and uses the stringification
  #It also uses the predefined macros __FILE__ and __LINE__ to indicate the source 
  #file and line number where the panic occurred. The do-while(0) construct ensures
  #that the macro behaves like a single statement and avoids dangling else problems.
def PANIC(msg) :                                             
    print("Panic: %s at %s:%d\n" % (msg, __file__, LINE()), file=sys.stderr) 
    exit(1)   

#UNIMPLEMENTED: A thing C-team had. Assuming it's for testing purposes?
#Using as a stand-in for WIP functions
def UNIMPLEMENTED(func) :
    print("Unimplemented: %s at line %d\n" % (func, LINE())); \
    exit(1);                                             

if __name__ == "__main__":
    print("Hello, World!")

#Start constructor, destructor, and other listed functions down here.

#dw_interface_create() creates and initializes a DWInterface
#   structure. It also initializes the libcurl library and creates a curl handle.
#Parameters:
#   username: A string containing the username for the DWInterface.
#   password: A string containing the password for the DWInterface.
#   env: ?
#   port: ?
#Returns:
#   A pointer to a DWInterface structure with allocated and copied username and
#       password fields, and a curl handle. If username or password are empty
#       strings, PANIC() is called and the program exits.

def dw_interface_create(username, password, env, port):
    UNIMPLEMENTED("create()")

#Set_UUIDs() seems to be essential for the UUIDs used throughout the other functions.
#For now, it's copied over directly from the C-team code.
def dw_interface_set_uuids(DWInterface *dwi,
                            const char source_uuid[UUID_LEN],
                            const char metric_uuid[UUID_LEN]) {
  if (!dwi->init) {
    PANIC(DWInterface must be initialized);
  }

  if (verify_uuid(source_uuid) != 0) {
    PANIC(invalid source_uuid);
  }
  if (verify_uuid(metric_uuid) != 0) {
    PANIC(invalid metric_uuid);
  }

  strcpy(dwi->uuids[0], source_uuid);
  strcpy(dwi->uuids[1], metric_uuid);
}
#commit_handshake() takes a JSON file to upload to the DataWarehouse and generates 2 UUIDs
#   and stores them in a char array. This function should be called before any data
#   insertion or query operations.
#Parameters:
#   dwi: a pointer to a DWInterface struct that contains information about the
#       current session.
#   json_file: a pointer to a FILE object that represents the JSON file.
#Return value:
#   A pointer to a char array that contains two UUIDs, each 36 bytes long.
def dw_interface_commit_handshake(dwi,json_file):
    if not dwi.init:   #init set to true after DWI created.
        PANIC("DWInterface must be initialized")

    if not dwi.uuids[0] or not dwi.uuids[1]:
        PANIC("DWInterface uuids must be set")
    UNIMPLEMENTED("commit_handshake()")


#insert_data() inserts new information into the DataWarehouse by sending a POST request
#   with a JSON file as the body.
#Parameters:
#   dwi: a pointer to a DWInterface struct that contains information about the
#        DataWarehouse connection.
#   source_uuid: the source uuid that is needed.
#   metric_uuid: the metric uuid that is needed.
#   json_file: a pointer to a FILE object that represents the JSON file.
# Return value:
#   An int value that indicates the status of the insertion operation.
#   (0 for success, non-zero for failure)
def dw_interface_insert_data(dwi, source_uuid, metric_uuid, json_file):
    UNIMPLEMENTED("insert_data()")

#retrieve_data() sends a query string to the DataWarehouse and returns a JSON-
#   formatted string as a result.
#Parameters:
#   dwi: a DWInterface struct that contains information about the DataWarehouse connection.
#   query_string: a pointer to a char array that contains the query string.
#Return value:
#   A pointer to a char array that contains the JSON formatted string returned by the DataWarehouse.

def dw_interface_retrieve_data(dwi, query_string):
    if not dwi.init:   #init set to true after DWI created.
        PANIC("DWInterface must be initialized")

    if not dwi.uuids[0] or not dwi.uuids[1]:
        PANIC("DWInterface uuids must be set")
    UNIMPLEMENTED("retrive_data()")
#...


#destroy()