#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define FILEPATH "../../sample.json"

int main(void) {
  FILE *fp = fopen(FILEPATH, "r");

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  dw_interface_set_uuids(dwi, "3e497c48-886f-44e6-b7e6-32b6c7b39a8b", "ae02e85a-21d8-41e7-93ab-70b08c47cf7a");

  fclose(fp);
  dw_interface_destroy(dwi);
  return 0;
}

