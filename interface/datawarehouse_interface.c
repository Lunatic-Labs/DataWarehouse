#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "datawarehouse_interface.h"

#define UNIMPLEMENTED printf("Unimplemented: %s at line %d\n", __func__, __LINE__)
#define PANIC(msg) do {                                                          \
  fprintf(stderr, "Panic: %s at %s:%d\n", msg, __FILE__, __LINE__);              \
  exit(EXIT_FAILURE);                                                            \
} while (0)

typedef struct DWInterface {
  char *usr;
  char *pass;
} DWInterface;

DWInterface *dw_interface_create(const char *usr, const char *pass) {
  size_t usr_sz  = strlen(usr);
  size_t pass_sz = strlen(pass);

  assert(usr_sz && pass_sz && "ERROR: username and password length must be at least 1.");

  DWInterface *dwi = malloc(sizeof(DWInterface));

  if (!dwi) {
    PANIC("Could not allocate DWInterface");
  }

  dwi->usr  = malloc(usr_sz  + 1);
  dwi->pass = malloc(pass_sz + 1);

  if (!dwi->usr || !dwi->pass) {
    PANIC("Could not allocate username or password");
  }

  strcpy(dwi->usr,  usr);
  strcpy(dwi->pass, pass);

  return dwi;
}

char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

int dw_interface_insert_data(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

char *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string) {
  UNIMPLEMENTED;
}

void dw_interface_destroy(DWInterface *dwi) {
  assert(dwi && "ERROR: dw_interface_create() must be called first");
  free(dwi->usr);
  free(dwi->pass);
  free(dwi);
}

