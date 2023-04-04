#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include "json.c"
#include "json.h"
#include "datawarehouse_config.h"
#include "../../interface/c_impl/datawarehouse_interface.h"
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

// TEST_GROUP()
// {
//     void setup();
//     void teardown();
// };

int main(void)
{
    struct Metric metric;
    struct Source source;
    struct Group group;

    DWInterface *dwi = dw_interface_create("usr", "pass", ENV_LOCAL, PORT_DEV);
    dw_interface_commit_handshake(dwi, handshake_json_filepath, out_json_filepath);
    dw_interface_insert_data(dwi, insert_json_filepath);

    FILE *fp;
    char buffer[1024];

    struct json_object *parsed_json;
    fp = fopen("out.json", "r");
    fread(buffer, 1024, 1, fp);
    fclose(fp);

    // Ask about how to use c json parser 
    // Found a json parse but need to know how to use and if it is good
    // https://github.com/json-parser/json-parser

    parsed_json = json_tokener_parse(buffer);

    
}
