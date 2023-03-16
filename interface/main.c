#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define HANDSHAKE_PATH "../../handshake.json"
#define INSERT_PATH "../../insert.json"

/* dw_interface_commit_handshake(dwi, handshake_file); */
/* dw_interface_insert_data(dwi, insert_file); */

int main(void) {

  FILE *handshake_file = fopen(HANDSHAKE_PATH, "r");
  FILE *insert_file = fopen(INSERT_PATH, "r");
  const char *query_string = "?class_gpa__eq=4";
  const char *group_uuid   = "0879623d-8595-4cd1-aaa0-80e850e563a1";
  const char *source_uuid  = "ac2f3f7f-ab0c-4393-a625-1e860731fa58";
  const char *metric_uuid  = "8b78534a-f559-4db6-8449-35c51c8bc1ab";

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);
  dw_interface_set_uuids(dwi, group_uuid, source_uuid, metric_uuid);

  const char *response = dw_interface_query_data(dwi, query_string);
  printf("RESPONSE: %s\n", response);

  dw_interface_destroy(dwi);
  fclose(handshake_file);
  fclose(insert_file);
  return 0;
}
