#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
// #include "../interface/c_impl/datawarehouse.h"
#include "../interface/c_impl/_datawarehouse_utils_INTERNAL.h"

/*
Goal is to create tests that will populate the database using the datawarehouse interface

Will need:
    - function to retrieve UUID's (Possible from JSON)

Research:
    - Lookup creating SRC files
*/

/*
Example of main
int main(void) {

  DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);

  Metric *m = dw_interface_metric_create(0, 4, "class_gpa", "GPA");
  Source *s = dw_interface_source_create("Python Class Stats");
  Group  *g = dw_interface_group_create("Academia", "My University");

  dw_interface_set_groups(dwi, g);

  dw_interface_destroy(dwi);
  return 0;
}
*/

TEST_GROUP()
{
    void setup();
    void teardown();
};

int main(void)
{
    struct Metric metric;
    struct Source source;
    struct Group group;
}
