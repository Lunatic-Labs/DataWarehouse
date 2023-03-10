#ifndef DATAWAREHOUSE_INTERFACE
#define DATAWAREHOUSE_INTERFACE

typedef struct DWInterface DWInterface;

DWInterface *dw_interface_create(const char *, const char *);

// Returns an array of size 2, each 36 chars long to hold both uuids.
char **dw_interface_commit_handshake(const DWInterface *, FILE *);
int    dw_interface_insert_data(const DWInterface *, FILE *);
char  *dw_interface_retrieve_data(const DWInterface *, const char *);
void   dw_interface_destroy(DWInterface *);

#endif // DATAWAREHOUSE_INTERFACE
