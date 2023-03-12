#include <stdio.h>
#include <string.h>
#include <errno.h>
#include "datawarehouse_interface.h"

#define FILEPATH "../../sample.json"

int main(void) {
  DWInterface *dwi = dw_interface_create("usr", "pass");

  FILE *json_file = fopen(FILEPATH, "r");

  if (!json_file) {
    fprintf (stderr, "Could not open %s\n", strerror(errno));
    return 1;
  }

  char **uuids = dw_interface_commit_handshake(dwi, json_file);

  dw_interface_destroy(dwi);

  return 0;
}
