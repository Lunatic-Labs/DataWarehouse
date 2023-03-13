#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define FILEPATH "../../sample.json"

<<<<<<< HEAD
int main(void) 
{
  const char *source_uuid = "tybrgvfecd";
  const char *metric_uuid = "ybihjknhgty";
  DWInterface *dwi = dw_interface_create("user", "pass");
  FILE* json_file = fopen("../../sample.json", "r");

  char** uuids = dw_interface_commit_handshake(dwi, json_file);

  //int i = dw_interface_insert_data(dwi, source_uuid, metric_uuid, json_file);
  
=======
int main(void) {
  FILE *fp = fopen(FILEPATH, "r");

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  dw_interface_set_uuids(dwi, "3e497c48-886f-44e6-b7e6-32b6c7b39a8b", "ae02e85a-21d8-41e7-93ab-70b08c47cf7a");

  fclose(fp);
>>>>>>> d3231386db3c3c9d8f38539258e01319bb26db16
  dw_interface_destroy(dwi);
  return 0;
}
