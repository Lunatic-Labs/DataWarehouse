#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define FILEPATH "../../sample.json"

int main(void) 
{
  const char *source_uuid = "tybrgvfecd";
  const char *metric_uuid = "ybihjknhgty";
  DWInterface *dwi = dw_interface_create("user", "pass");
  FILE* json_file = fopen("../../sample.json", "r");

  char** uuids = dw_interface_commit_handshake(dwi, json_file);

  //int i = dw_interface_insert_data(dwi, source_uuid, metric_uuid, json_file);
  
  dw_interface_destroy(dwi);

  return 0;
}
