/*
 * This is the function declarations for the DataWarehouse interface.
 * This file is for external use.
 */

#include "_datawarehouse_utils_INTERNAL.h"

#ifndef DATAWAREHOUSE_INTERFACE
#define DATAWAREHOUSE_INTERFACE

typedef struct DWInterface DWInterface;

void debug(DWInterface *dwi);

// Creates a new instance of the DWInterface struct.
// It takes a username and password and puts them in the DWInterface.
// It also takes an environment to determine where the server is.
// It also takes a port to determine which database we are working with.
// This function will PANIC if one of the following occurs:
//   1. Username and/or password are not of length 1 or more.
//   2. malloc() failure.
//   3. CURL failure.
//   4. An invalid PORT is provided.
//   5. An invalid ENV is provided.
DWInterface *dw_interface_create(char *username, char *password, enum ENV env, enum PORT port);

// Performs a handshake request on the database.
// It will return the response from the POST request (your handshake data)
// as a `char *`. You can also specify `out_filepath` which, if not NULL, will
// write the data to a file location you specify. Leave NULL if you do not want
// a file. This function handles all I/O including opening and closing.
// This function will PANIC if one of the following occurs:
//   1. File I/O failure.
//   2. malloc() failure.
//   3. CURL failure.
char *dw_interface_commit_handshake(const DWInterface *dwi, const char *handshake_json_filepath, const char *out_filepath);

// Inserts data into the database. A source uuid and a metric uuid must be provided.
// If you need these, then perform dw_interface_commit_handshake().
// This function will PANIC if one of the following occurs:
//   1. File I/O failure.
//   2. malloc() failure.
//   3. CURL failure.
void dw_interface_insert_data(const DWInterface *dwi, const char *insert_json_filepath);

// Call this function if you already have predetermined uuids. If not,
// you can obtain these uuids through dw_interface_commit_handshake().
// This function MUST be called before dw_interface_query_data().
// This function will PANIC if the provided UUIDs are not valid.
void dw_interface_set_uuids(DWInterface *dwi, const char group_uuid[36], const char source_uuid[36], const char metric_uuid[36]);

// Querys tables in the database.
// It will return the response from the GET request (your query)
// as a `char *`. You can also specify `out_filepath` which, if not NULL, will
// write the data to a file location you specify. Leave NULL if you do not want
// a file. This function handles all I/O including opening and closing.
// This function will PANIC if one of the following occurs:
//   1. UUIDs are not present.
//   2. File I/O failure.
//   3. The query string does not start with '?'.
//   4. malloc() failure.
//   5. CURL failure.
char *dw_interface_query_data(const DWInterface *dwi, const char *query_string, const char *out_filepath);

// Free()'s all memory allocated. This function
// will PANIC if DWInterface has not been initialized.
void dw_interface_destroy(DWInterface *dwi);

void dw_interface_set_groups(DWInterface *dwi, Group *groups);

Group *dw_interface_group_create(char *classification, char *group_name);

Source *dw_interface_source_create(char *name);

Metric *dw_interface_metric_create(int asc, Datatype data_type, char *name, char *units);

void dw_interface_push_group(DWInterface *dwi, Group *group);

void dw_interface_push_source(Group *group, Source *source);

void dw_interface_push_metric(Source *source, Metric *metric);

#endif // DATAWAREHOUSE_INTERFACE
