#ifndef DATAWAREHOUSE_INTERFACE
#define DATAWAREHOUSE_INTERFACE

typedef struct DWInterface DWInterface;

DWInterface *dw_interface_create(const char *username, const char *password);

// Returns an array of size 2, each 36 chars long to hold both uuids.
char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_file);
int    dw_interface_insert_data(const DWInterface *dwi,
                                const char *source_uuid,
                                const char *metric_uuid,
                                FILE *json_file);
char  *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string);
void   dw_interface_destroy(DWInterface *dwi);

#endif // DATAWAREHOUSE_INTERFACE
