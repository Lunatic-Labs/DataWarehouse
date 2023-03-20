#include <stdio.h>
#include <stdlib.h>
#include "datawarehouse_interface.h"

// First call: the function: dw_interface_create(usr, pass, env, port);
// Then call: dw_interface_commit_handshake(dwi, handshake_json_filepath, out_filepath);

// Make sure to create your insert file with the output from the handshake.
// Then call: dw_interface_insert_data(dwi, insert_json_filepath);

// Set UUIDs:
#define GUUID ""
#define SUUID ""
#define MUUID ""
// Then call: dw_interface_set_uuids(dwi, GUUID, SUUID, MUUID);
// then call: dw_interface_query_data(dwi, qstring, query_out_filepath);


void handshake(DWInterface *dwi, const char *handshake_filepath, const char *out_filepath) {
  dw_interface_commit_handshake(dwi, handshake_filepath, out_filepath);
}

void insert(DWInterface *dwi, const char *insert_json_filepath) {
  dw_interface_insert_data(dwi, insert_json_filepath);
}

char *query(DWInterface *dwi, const char *qstring, const char *query_out_filepath) {
  dw_interface_set_uuids(dwi, GUUID, SUUID, MUUID);
  char *response = dw_interface_query_data(dwi, qstring, query_out_filepath);
  return response;
}

int main(void) {

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  const char *handshake_filepath     = "../../../handshake.json";
  const char *insert_filepath        = "../../../insert.json";
  const char *query_out_filepath     = "query.out";
  const char *handshake_out_filepath = "handshake.out";
  const char *qstring                = "?";

  dw_interface_destroy(dwi);
  return 0;
}
