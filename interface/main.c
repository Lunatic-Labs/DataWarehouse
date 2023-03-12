#include <stdio.h>
#include "datawarehouse_interface.h"

int main(void) {
  DWInterface *dwi = dw_interface_create("usr", "pass");
  dw_interface_destroy(dwi);
  return 0;
}
