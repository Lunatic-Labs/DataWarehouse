#include <assert.h> // Could be useful?
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <curl/curl.h> // NOTE: To install: sudo apt install libcurl4-openssl-dev
#include "datawarehouse_interface.h"

#define UNIMPLEMENTED printf("Unimplemented: %s at line %d\n", __func__, __LINE__)

// PANIC macro. Provide a string or nothing to
// print a reason for crashing abruptly.
#define PANIC(msg) do {                                                          \
  fprintf(stderr, "Panic: %s at %s:%d\n", #msg, __FILE__, __LINE__);             \
  exit(EXIT_FAILURE);                                                            \
} while (0)

struct buffer_t {
  char  *data;
  size_t size;
  size_t max;
};

// Our main `object` that we are dealing with.
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

// Private. Strictly used for constructing a `buffer_t`.
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

// Public. This is the first function that should be called by the user.
// This function acts as a constructor for the `DWInterface` object.
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

// Public. The goal of this function is to provide the DataWarehouse
// with a properly formatted JSON file. This function MUST be called
// first, before inserting/querying data. The function should return
// 2 uuid's, each 36 bytes long. Maybe we should have UUID's be member
// variables of the DWInterface struct?
char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

// Public. The goal of this function is to insert new information
// into the DataWarehouse. Note that it takes a `FILE*` and not a `char*`.
// This is to allow support for a file located not in the CWD.
int dw_interface_insert_data(const DWInterface *dwi, FILE *json_filepath) {
  UNIMPLEMENTED;
}

// Public. The goal of this function is to provide it with a `query_string`
// and it will send it to the DataWarehouse, hopefully getting back a JSON
// formatted string (char*).
char *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string) {
  struct buffer_t buf = buffer_t_create(1024);
  curl_easy_setopt(dwi->curl, CURLOPT_WRITEFUNCTION, callback);
  curl_easy_setopt(dwi->curl, CURLOPT_WRITEDATA,     &buf);
  curl_easy_setopt(dwi->curl, CURLOPT_URL,           query_string); // Using query_string as a placeholder.

  CURLcode curl_code = curl_easy_perform(dwi->curl);

  if (curl_code != CURLE_OK) {
    fprintf(stderr, "ERROR: curl_easy_perform() failed. Reason: %s\n",
            curl_easy_strerror(curl_code));
    PANIC();
  }

  char *data = buf.data; // Do something with data?
  free(buf.data);
  return data;
}

// Public. This is the last function that should be
// called by the user. Free()'s up all memory.
void dw_interface_destroy(DWInterface *dwi) {
  if (!dwi) {
    PANIC(dw_interface_create() must be called first);
  }
  curl_easy_cleanup(dwi->curl);
  free(dwi->username);
  free(dwi->password);
  free(dwi);
}

