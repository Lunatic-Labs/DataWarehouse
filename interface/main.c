#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define FILEPATH "../../handshake.json"

const char *metric_uuid = "3e182307-ac47-4a92-b577-420b028aa583";
const char *source_uuid = "902d2844-96c9-4249-8160-bd1158e8eaae";
const char *group_uuid  = "3ada724c-7725-48c2-9133-a7bafd026803";

const char *query_string = "?temperature__<100";

int main(void) {
  FILE *fp = fopen(FILEPATH, "r");
  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);
  dw_interface_set_uuids(dwi, group_uuid, source_uuid, metric_uuid);

  char *data = dw_interface_query_data(dwi, query_string);

  (void)data;

  fclose(fp);
  dw_interface_destroy(dwi);
  return 0;
}

