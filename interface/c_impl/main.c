#include <stdio.h>
#include <stdlib.h>
#include "datawarehouse_interface.h"

int main(void) {

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  Metric *m = dw_interface_metric_create(0, 4, "class_gpa", "GPA");
  Source *s = dw_interface_source_create("Python Class Stats", m);
  Group  *g = dw_interface_group_create("Academia", "My University", s);

  dw_interface_set_groups(dwi, g);

  dw_interface_destroy(dwi);
  return 0;
}
