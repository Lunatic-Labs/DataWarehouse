#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h> // NOTE: To install: sudo apt install libcurl4-openssl-dev
#include "datawarehouse_interface.h"

#define UNIMPLEMENTED printf("Unimplemented: %s at line %d\n", __func__, __LINE__)
#define PANIC(msg) do {                                                          \
  fprintf(stderr, "Panic: %s at %s:%d\n", msg, __FILE__, __LINE__);              \
  exit(EXIT_FAILURE);                                                            \
} while (0)

struct buffer_t {
  char *data;
  size_t size;
  size_t max;
};

typedef struct DWInterface {
  char *username;
  char *password;
  CURL *curl;
} DWInterface;

struct buffer_t buffer_t_create(size_t m) {
  struct buffer_t buff;
  buff.data = malloc(m * sizeof(char));
  buff.size = 0;
  buff.max  = m;
  return buff;
}

// Private. Used for data retrieval.
size_t receive_data(void *contents, size_t size, size_t nmemb, void *context) {
  struct buffer_t *b = (struct buffer_t *)context;
  size_t real_size = size * nmemb;

  b->data = !b->data ?
    malloc(real_size)
    : realloc(b->data, b->size + real_size);

  memcpy(b->data + b->size, contents, real_size);
  b->size += real_size;

  return real_size;
}

DWInterface *dw_interface_create(const char *username, const char *password) {
  size_t usr_sz  = strlen(username);
  size_t pass_sz = strlen(password);

  assert(usr_sz && pass_sz && "ERROR: username and password length must be at least 1.");

  DWInterface *dwi = malloc(sizeof(DWInterface));

  if (!dwi) {
    PANIC("Could not allocate DWInterface");
  }

  dwi->username  = malloc(usr_sz  + 1);
  dwi->password = malloc(pass_sz + 1);

  if (!dwi->username || !dwi->password) {
    PANIC("Could not allocate username or password");
  }

  strcpy(dwi->username,  username);
  strcpy(dwi->password, password);

  // Init curl/curl.h library.
  curl_global_init(CURL_GLOBAL_ALL);

  dwi->curl = curl_easy_init();

  return dwi;
}

char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_filepath) {

}

int dw_interface_insert_data(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

char *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string) {
  UNIMPLEMENTED;
}

void dw_interface_destroy(DWInterface *dwi) {
  assert(dwi && "ERROR: dw_interface_create() must be called first");
  free(dwi->username);
  free(dwi->password);
  free(dwi);
}

