#include <stdio.h>
#include "datawarehouse_interface.h"

int main(void) {

  DWInterface *dwi = dw_interface_create("usr", "pass");
  char *data = dw_interface_retrieve_data(dwi, "https://www.debian.org/");
  dw_interface_destroy(dwi);

  return 0;
}
