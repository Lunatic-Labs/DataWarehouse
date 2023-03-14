#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define FILEPATH "../../handshake.json"

const char *group_uuid  = "96527922-c8db-45e9-85f4-3e6d2613d698";
const char *source_uuid = "45659d3a-3359-46cd-98af-7a130598fa9b";
const char *metric_uuid = "c61d91ac-f26c-4ddf-8bf7-f71ccafb8406";

const char *query_string = "?limit=1";

int main(void) {
  FILE *fp = fopen(FILEPATH, "r");

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  dw_interface_commit_handshake(dwi, fp);

  dw_interface_set_uuids(dwi, group_uuid, source_uuid, metric_uuid);

  char *data = dw_interface_query_data(dwi, query_string);
  printf("%s\n", data);

  fclose(fp);
  dw_interface_destroy(dwi);
  return 0;
}
