#include <stdio.h>
#include <stdlib.h>
#include "datawarehouse_interface.h"

int main(void) {

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  for (int i = 0; i < 1000; i++) {
    Group *g = dw_interface_group_create("class", "name");
    dw_interface_push_group(dwi, g);
  }

  debug(dwi);

  dw_interface_destroy(dwi);

  return 0;
}
