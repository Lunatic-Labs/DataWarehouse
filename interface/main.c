#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define HANDSHAKE_JSON "../../handshake.json"
#define INSERT_JSON "../../insert.json"

const char *group_uuid  = "2d41cd1f-6bed-45e0-b94c-a2429bc81fae";
const char *source_uuid = "5e1f1a24-f7b6-4793-b366-145aa256311e";
const char *metric_uuid = "ee2d77e1-209e-4e97-a658-574030c403c4";

const char *query_string = "?limit=1";
/* dw_interface_commit_handshake(dwi, handshake_json); */

int main(void) {
  FILE *handshake_json = fopen(HANDSHAKE_JSON, "r");
  FILE *insert_json    = fopen(INSERT_JSON, "r");

  if (!handshake_json) {
    fprintf(stderr, "ERROR: could not open file. Reason: %s\n", strerror(errno));
  }

  if (!insert_json) {
    fprintf(stderr, "ERROR: could not open file. Reason: %s\n", strerror(errno));
  }

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  dw_interface_insert_data(dwi, insert_json);




  fclose(handshake_json);
  fclose(insert_json);
  dw_interface_destroy(dwi);
  return 0;
}
