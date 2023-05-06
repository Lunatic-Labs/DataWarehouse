#include <stdio.h>
#include <stdlib.h>
#include "datawarehouse_interface.h"

int main(void) {
  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  char *json_filepath = "handshake.out";
  char *source_name   = "Python Class Stats";
  char *metric_name   = "students_present";
  int val = 5;

  char *res = json_parser(json_filepath, source_name, metric_name, val);

  (void)res;

  dw_interface_destroy(dwi);
  return 0;
}
