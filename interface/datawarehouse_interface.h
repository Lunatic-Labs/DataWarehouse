#ifndef DATAWAREHOUSE_INTERFACE
#define DATAWAREHOUSE_INTERFACE

typedef struct DWInterface DWInterface;

// Ports. This is to determine which database we will
// be sending information to/from. We will mostly be
// working in PORT_DEV.
enum PORT {
  PORT_DEV,
  PORT_STAGING,
  PORT_PROD,
};

// Environments. Use ENV_LOCAL if the server is
// running locally.
enum ENV {
  ENV_LOCAL,
  ENV_REMOTE
};

// Creates a new instance of the DWInterface struct.
// It takes a username and password and puts them in the DWInterface.
// It also takes an environment to determine where the server is.
// It also takes a port to determine which database we are working with.
DWInterface *dw_interface_create(const char *username, const char *password, enum ENV env, enum PORT port);

// Performs a handshake request on the database. Gives back 2 36 byte uuids.
char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_file);

// Inserts data into the database. A source uuid and a metric uuid must be provided.
// If you need these, then perform dw_interface_commit_handshake().
int dw_interface_insert_data(const DWInterface *dwi, const char *source_uuid, const char *metric_uuid, FILE *json_file);

// Querys tables in the database.
char *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string);

// Call this function if you already have predetermined uuids. If not,
// you can obtain these uuids through dw_interface_commit_handshake().
void dw_interface_set_uuids(DWInterface *dwi, const char source_uuid[36], const char metric_uuid[36]);

// Free()'s all memory allocated.
void dw_interface_destroy(DWInterface *dwi);

#endif // DATAWAREHOUSE_INTERFACE
