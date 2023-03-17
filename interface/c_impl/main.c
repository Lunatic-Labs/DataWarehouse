#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>

#include "datawarehouse_interface.h"

int main(void) {

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  dw_interface_destroy(dwi);
  return 0;
}
