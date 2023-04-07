#include <stdio.h>
#include <stdlib.h>
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "datawarehouse_config.h"
#include "../../interface/c_impl/datawarehouse_interface.h"
/*
Goal is to create tests that will populate the database using the datawarehouse interface

Will need:
    - function to retrieve UUID's (Possible from JSON)

Research:
    - Pep 7 coding standard for implementing c code with python
        https://peps.python.org/pep-0007/
        - May not be neccessary but need to look to be sure
    - Python/C API
        https://docs.python.org/3/c-api/intro.html

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


int main(void)
{
    struct Metric metric;
    struct Source source;
    struct Group group;

    DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);
    dw_interface_commit_handshake(dwi, handshake_json_filepath, out_json_filepath);
    dw_interface_insert_data(dwi, insert_json_filepath);

    
}
