#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h> // NOTE: To install: sudo apt install libcurl4-openssl-dev
#include "datawarehouse_interface.h"

#define UNIMPLEMENTED printf("Unimplemented: %s at line %d\n", __func__, __LINE__)
#define PANIC(msg) do {                                                          \
  fprintf(stderr, "Panic: %s at %s:%d\n", #msg, __FILE__, __LINE__);             \
  exit(EXIT_FAILURE);                                                            \
} while (0)

struct buffer_t {
  char  *data;
  size_t size;
  size_t max;
};

typedef struct DWInterface {
  char *username;
  char *password;
  CURL *curl;
} DWInterface;

// Private. A safer malloc() to eliminate checking
// whether or not malloc() returned successfully.
static void *s_malloc(size_t nbytes) {
  void *p = malloc(nbytes);
  if (!p) {
    fprintf(stderr, "ERROR: failed to allocate %zu bytes. Reason: %s\n",
            nbytes, strerror(errno));
    PANIC();
  }
  return p;
}

// Private. A safer realloc() to eliminate checking
// whether or not realloc() returned successfully.
static void *s_realloc(void *ptr, size_t nbytes) {
  void *p = realloc(ptr, nbytes);
  if (!p) {
    fprintf(stderr, "ERROR: failed to reallocate %zu bytes. Reason: %s\n",
            nbytes, strerror(errno));
    PANIC();
  }
  return p;
}

struct buffer_t buffer_t_create(size_t m) {
  struct buffer_t buff;
  buff.data = s_malloc(m * sizeof(char));
  buff.size = 0;
  buff.max  = m;
  return buff;
}

// Private. Used for data retrieval.
static size_t callback(void *contents, size_t size, size_t nmemb, void *context) {
  struct buffer_t *b = (struct buffer_t *)context;
  size_t real_size = size * nmemb;

  b->data = !b->data ?
    s_malloc(real_size + 1)
    : s_realloc(b->data, b->size + real_size + 1);

  memcpy(b->data + b->size, contents, real_size);
  b->size += real_size;
  b->data[b->size] = '\0';

  return real_size;
}

DWInterface *dw_interface_create(const char *username, const char *password) {
  size_t usr_len  = strlen(username);
  size_t pass_len = strlen(password);

  if (!usr_len || !pass_len) {
    PANIC(username and password length must be at least 1);
  }

  DWInterface *dwi = s_malloc(sizeof(DWInterface));

  dwi->username = s_malloc(usr_len  + 1);
  dwi->password = s_malloc(pass_len + 1);

  strcpy(dwi->username, username);
  strcpy(dwi->password, password);

  // Init curl/curl.h library.
  curl_global_init(CURL_GLOBAL_ALL);

  // Create curl.
  dwi->curl = curl_easy_init();

  return dwi;
}

char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

int dw_interface_insert_data(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

char *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string) {
  struct buffer_t buf = buffer_t_create(1024);
  curl_easy_setopt(dwi->curl, CURLOPT_WRITEFUNCTION, callback);
  curl_easy_setopt(dwi->curl, CURLOPT_WRITEDATA,     &buf);
  curl_easy_setopt(dwi->curl, CURLOPT_URL,           query_string); // Using query_string as a placeholder.

  CURLcode curl_code = curl_easy_perform(dwi->curl);

  if (curl_code != CURLE_OK) {
    PANIC(curl did not succeed);
  }

  char *data = buf.data; // Do something with data?
  free(buf.data);
  return data;
}

void dw_interface_destroy(DWInterface *dwi) {
  if (!dwi) {
    PANIC(dw_interface_create() must be called first);
  }
  curl_easy_cleanup(dwi->curl);
  free(dwi->username);
  free(dwi->password);
  free(dwi);
}

