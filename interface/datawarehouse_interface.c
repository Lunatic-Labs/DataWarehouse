#include <assert.h> // Could be useful.
#include <errno.h>
#include <regex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// NOTE: To install: sudo apt install libcurl4-openssl-dev
// NOTE: Documentation: https://curl.se/libcurl/c/
#include <curl/curl.h>

#include "datawarehouse_interface.h"

#define REMOTE_IP_ADDR "54.159.108.136"
#define LOCAL_IP_ADDR  "127.0.0.1"

#define DEVELOPMENT_PORT ":5000"
#define STAGING_PORT     ":4000"
#define PRODUCTION_PORT  ":3000"

#define HANDSHAKE_PATH "/api/prepare/"
#define INSERT_PATH    "/api/store/"
#define QUERY_PATH     "/api/query/"

#define UUID_LEN 36

#define NOP(x)         (void)(x);
#define UNIMPLEMENTED  printf("Unimplemented: %s at line %d\n", __func__, __LINE__); \
  exit(EXIT_FAILURE);

#define EXISTS(ptr) do {                        \
  if (!ptr) {                                   \
    PANIC(null pointer: #ptr);                  \
  }                                             \
} while (0)

// Do not touch.
char *GLOBAL_AUTHORITY;

/*
 * PANIC: A macro that prints an error message and exits the program with a
 * failure status. It takes a message as an argument and uses the stringification
 * operator (#) to convert it to a string literal. It also uses the predefined
 * macros __FILE__ and __LINE__ to indicate the source file and line number where
 * the panic occurred. The do-while(0) construct ensures that the macro behaves
 * like a single statement and avoids dangling else problems.
 */
#define PANIC(msg) do {                                              \
  fprintf(stderr, "Panic: %s at %s:%d\n", #msg, __FILE__, __LINE__); \
  exit(EXIT_FAILURE);                                                \
} while (0)

// TODO: Instead of calling PANIC() whenever a fatal error occurs, we should
//       eventually move to using error codes and have a better way to handle
//       errors or failures.
enum ErrorCode {
  OK = 1,
};

/*
 * buffer_t: A structure that represents a dynamic buffer of characters. It
 * contains fields for the data array, the current size of the buffer, and the
 * maximum size of the buffer. The data array is allocated and resized using
 * s_malloc and s_realloc functions. The size field indicates how many bytes are
 * currently stored in the buffer. The max field indicates how many bytes can be
 * stored in the buffer without resizing it.
 */
struct buffer_t {
  char  *data;
  size_t size;
  size_t max;
};

/*
 * DWInterface: A structure that represents a DataWarehouse interface. It contains
 * fields for the username and password of the user, and a curl handle for
 * making HTTP requests to the DataWarehouse server.
 */
typedef struct DWInterface {
  char *username;
  char *password;
  char uuids[2][UUID_LEN + 1];
  CURL *curl_handle;
  enum ENV env;
  enum PORT port;
  int init;
} DWInterface;

/*
 * s_malloc: A wrapper function for malloc that checks for allocation errors
 * and exits the program if any occur.
 * Parameters:
 *   nbytes: The size of the memory block to be allocated in bytes.
 * Returns:
 *   A pointer to the allocated memory block. The content of the block is
 *   uninitialized.
 */
static void *s_malloc(size_t nbytes) {
  void *p = malloc(nbytes);
  if (!p) {
    fprintf(stderr, "ERROR: failed to allocate %zu bytes. Reason: %s\n",
            nbytes, strerror(errno));
    PANIC();
  }
  return p;
}

/*
 * s_realloc: A wrapper function for realloc that checks for allocation errors
 * and exits the program if any occur.
 * Parameters:
 *   ptr: A pointer to the memory block to be reallocated, or NULL if a new
 *        block is requested.
 *   nbytes: The new size of the memory block in bytes.
 * Returns:
 *   A pointer to the reallocated memory block, which may be different from ptr.
 *   The original content of the block is preserved up to the minimum of the old
 *   and new sizes.
 */
static void *s_realloc(void *ptr, size_t nbytes) {
  void *p = realloc(ptr, nbytes);
  if (!p) {
    fprintf(stderr, "ERROR: failed to reallocate %zu bytes. Reason: %s\n",
            nbytes, strerror(errno));
    PANIC();
  }
  return p;
}

/*
 * verify_uuid: A function that checks if a string is a valid UUID.
 * Parameters:
 *   uuid: The string to be checked.
 * Returns:
 *   0 if the string is a valid UUID, REG_NOMATCH if it is not, or a
 *   nonzero error code if an error occurs.
 * NOTE: We may not need this function, but it's here just in case.
 */
static int verify_uuid(const char *uuid) {
  regex_t regex;
  regcomp(&regex,
          "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
          REG_EXTENDED
          | REG_NOSUB
          | REG_ICASE);
  return regexec(&regex, uuid, (size_t)0, NULL, (int)0);
}

/*
 * buffer_t_create: A function that creates and initializes a buffer_t structure.
 * Parameters:
 *   m: The maximum size of the buffer in bytes.
 * Returns:
 *   A buffer_t structure with an allocated data array of size m, a size of 0,
 *   and a max of m.
 */
struct buffer_t buffer_t_create(size_t m) {
  struct buffer_t buff;
  buff.data = s_malloc(m * sizeof(char));
  buff.size = 0;
  buff.max  = m;
  return buff;
}

/*
 * callback: A function that appends the contents of a data chunk to a buffer_t
 * structure. It is intended to be used as a write callback function for
 * libcurl.
 * Parameters:
 *   contents: A pointer to the data chunk received by libcurl.
 *   size: The size of each element in the data chunk in bytes.
 *   nmemb: The number of elements in the data chunk.
 *   context: A pointer to a buffer_t structure where the data chunk will be
 *            appended.
 * Returns:
 *   The number of bytes actually appended to the buffer_t structure, which
 *   should be equal to size*nmemb unless an allocation error occurs. In that
 *   case, PANIC() is called and the program exits.
 */
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

/* This function builds an IP address based on the environment and port specified.
 * Parameters:
 *   dwi: a pointer to a DWInterface.
 */
static void build_GLOBAL_AUTHORITY(const DWInterface *dwi) {

  // Set the protocol to http.
  const char *protocol = "http://", *port, *ip_addr;

  // Set the IP address based on the environment.
  switch (dwi->env) {
    case ENV_REMOTE:
      ip_addr = REMOTE_IP_ADDR;
      break;
    case ENV_LOCAL:
      ip_addr = LOCAL_IP_ADDR;
      break;
    default:
      PANIC(invalid environment);
  }

  // Set the port based on the specified port.
  switch (dwi->port) {
    case PORT_DEV:
      port = DEVELOPMENT_PORT;
      break;
    case PORT_STAGING:
      port = STAGING_PORT;
      break;
    case PORT_PROD:
      port = PRODUCTION_PORT;
      break;
    default:
      PANIC(invalid port);
  }

  // Calculate the length of the protocol, IP address, and port.
  size_t protocol_len = strlen(protocol);
  size_t ip_addr_len  = strlen(ip_addr);
  size_t port_len     = strlen(port);

  // Calculate the total length of the authority string.
  size_t total_len = protocol_len + ip_addr_len + port_len + 1;
  GLOBAL_AUTHORITY = s_malloc(total_len);

  // Initialize the authority string to all '\0'.
  memset(GLOBAL_AUTHORITY, '\0', total_len);

  // Copy the protocol, IP address, and port into the authority string.
  strcpy(GLOBAL_AUTHORITY, protocol);
  strcat(GLOBAL_AUTHORITY, ip_addr);
  strcat(GLOBAL_AUTHORITY, port);
}

/*
 * construct_url: A function that constructs a URL by concatenating a global
 * authority with a given path.
 * Parameters:
 *   path: A string containing the path to be appended to the global authority.
 * Returns:
 *   A pointer to a newly allocated string containing the constructed URL. The
 *   URL is formed by concatenating the global authority (GLOBAL_AUTHORITY) with
 *   the given path. Memory for the new string is allocated using s_malloc and
 *   must be freed by the caller.
 */
static char *construct_url(const char *path) {
  char *url = s_malloc(strlen(GLOBAL_AUTHORITY) + strlen(path) + 1);
  strcpy(url, GLOBAL_AUTHORITY);
  strcat(url, path);
  return url;
}

/*
 * dw_interface_create: A function that creates and initializes a DWInterface
 * structure. It also initializes the libcurl library and creates a curl handle.
 * Parameters:
 *   username: A string containing the username for the DWInterface.
 *   password: A string containing the password for the DWInterface.
 * Returns:
 *   A pointer to a DWInterface structure with allocated and copied username and
 *   password fields, and a curl handle. If username or password are empty
 *   strings, PANIC() is called and the program exits.
 */
DWInterface *dw_interface_create(const char *username,
                                 const char *password,
                                 enum ENV env,
                                 enum PORT port) {
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
  dwi->curl_handle = curl_easy_init();

  dwi->env  = env;
  dwi->port = port;

  dwi->uuids[0][0] = '\0';
  dwi->uuids[1][0] = '\0';

  // Build the GLOBAL_AUTHORITY.
  build_GLOBAL_AUTHORITY(dwi);

  dwi->init = 1;

  return dwi;
}

void dw_interface_set_uuids(DWInterface *dwi,
                            const char source_uuid[UUID_LEN],
                            const char metric_uuid[UUID_LEN]) {
  if (!dwi->init) {
    PANIC(DWInterface must be initialized);
  }

  if (verify_uuid(source_uuid) != 0) {
    PANIC(invalid source_uuid);
  }
  if (verify_uuid(metric_uuid) != 0) {
    PANIC(invalid metric_uuid);
  }

  strcpy(dwi->uuids[0], source_uuid);
  strcpy(dwi->uuids[1], metric_uuid);
}

/*
 * This function takes a JSON file to upload to the DataWarehouse and generates 2 UUIDs
 * and storing them in a char array. This function should be called before any data
 * insertion or query operations.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that contains information about the
 *        current session.
 *   json_file: a pointer to a FILE object that represents the JSON file.
 * Return value:
 *   A pointer to a char array that contains two UUIDs, each 36 bytes long.
 */
char **dw_interface_commit_handshake(const DWInterface *dwi, FILE *json_file) {
  if (!dwi->init) {
    PANIC(DWInterface must be initialized);
  }

  if (!dwi->uuids[0] || !dwi->uuids[1]) {
    PANIC(DWInterface uuids must be set);
  }

  char **uuids = NULL, *file_data = NULL;
  struct curl_slist *headers = NULL;
  size_t file_size;
  CURLcode curl_code;

  // Construct a valid url with the GLOBAL_AUTHORITY and the HANDSHAKE_PATH.
  char *url = construct_url(HANDSHAKE_PATH);

  uuids        = s_malloc(sizeof(char *) * 2);
  *(uuids + 0) = s_malloc(sizeof(char)   * (UUID_LEN + 1));
  *(uuids + 1) = s_malloc(sizeof(char)   * (UUID_LEN + 1));

  curl_easy_setopt(dwi->curl_handle, CURLOPT_URL,  url);
  curl_easy_setopt(dwi->curl_handle, CURLOPT_POST, 1L);

  // Set the content type header to application/json.
  headers = curl_slist_append(headers, "Content-Type: application/json");
  curl_easy_setopt(dwi->curl_handle, CURLOPT_HTTPHEADER, headers);

  // Get the size of the file.
  fseek(json_file, 0, SEEK_END);
  file_size = ftell(json_file);
  rewind(json_file);

  // Get the file data.
  file_data = malloc(file_size + 1);
  if (!fread(file_data, 1, file_size, json_file)) {
    fprintf(stderr, "ERROR: Failed to read file contents. Reason: %s\n",
            strerror(errno));
    PANIC();
  }
  file_data[file_size] = '\0';

  // Set the request body to the file contents.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_POSTFIELDS, file_data);

  // Set the request body size to the size of the file.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_POSTFIELDSIZE, file_size);

  curl_code = curl_easy_perform(dwi->curl_handle);
  if (curl_code != CURLE_OK) {
    fprintf(stderr, "ERROR: curl_easy_perform() failed. Reason: %s\n",
            curl_easy_strerror(curl_code));
    PANIC();
  }

  curl_slist_free_all(headers);

  // TODO: assign UUIDs.
  // TODO: maybe write UUIDs to a file.

  free(url);
  return uuids;
}

/*
 * This function inserts new information into the DataWarehouse by sending a POST request
 * with a JSON file as the body.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that contains information about the
 *        DataWarehouse connection.
 *   source_uuid: the source uuid that is needed.
 *   metric_uuid: the metric uuid that is needed.
 *   json_file: a pointer to a FILE object that represents the JSON file.
 * Return value:
 *   An int value that indicates the status of the insertion operation.
 *   (0 for success, non-zero for failure)
 */
int dw_interface_insert_data(const DWInterface *dwi,
                             const char *source_uuid,
                             const char *metric_uuid,
                             FILE *json_file) {
  if (!dwi->init) {
    PANIC(DWInterface must be initialized);
  }

  if (!dwi->uuids[0] || !dwi->uuids[1]) {
    PANIC(DWInterface uuids must be set);
  }

  NOP(dwi); NOP(source_uuid); NOP(metric_uuid); NOP(json_file);

  // Construct a valid url with the GLOBAL_AUTHORITY and the INSERT_PATH.
  char *url = construct_url(INSERT_PATH);
  NOP(url);

  UNIMPLEMENTED;

  free(url);
  return 0;
}

/*
 * This function sends a query string to the DataWarehouse and returns a JSON
 * formatted string as a result.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that contains information about
 *        the DataWarehouse connection.
 *   query_string: a pointer to a char array that contains the query string.
 * Return value:
 *   A pointer to a char array that contains the JSON formatted string
 *   returned by the DataWarehouse.
 */
char *dw_interface_retrieve_data(const DWInterface *dwi, const char *query_string) {

  if (!dwi->init) {
    PANIC(DWInterface must be initialized. Call dw_interface_create());
  }

  if (!dwi->uuids[0] || !dwi->uuids[1]) {
    PANIC(DWInterface uuids must be set);
  }

  // Construct a valid url with the GLOBAL_AUTHORITY and the QUERY_PATH.
  char *url = construct_url(QUERY_PATH);

  printf("%s\n", url);

  NOP(query_string); NOP(url);

  // The code below will curl the url (in this case LOCALHOST_QUERY_URL)
  // and any information that curl gets is stored in a `char *`. This is
  // return and the user can do what they want with it.

  UNIMPLEMENTED;

  struct buffer_t buf = buffer_t_create(1024);

  curl_easy_setopt(dwi->curl_handle, CURLOPT_WRITEFUNCTION, callback);
  curl_easy_setopt(dwi->curl_handle, CURLOPT_WRITEDATA,     &buf);
  /* curl_easy_setopt(dwi->curl_handle, CURLOPT_URL,           LOCALHOST_QUERY_URL); // Replace this. */

  CURLcode curl_code = curl_easy_perform(dwi->curl_handle);

  if (curl_code != CURLE_OK) {
    fprintf(stderr, "ERROR: curl_easy_perform() failed. Reason: %s\n",
            curl_easy_strerror(curl_code));
    PANIC();
  }

  char *data = buf.data; // Do something with data?
  free(buf.data);
  free(url);
  return data;
}

/*
 * This function frees up all the memory allocated by the DWInterface struct and its fields.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that needs to be destroyed.
 * Return value:
 *   None
 */
void dw_interface_destroy(DWInterface *dwi) {
  if (!dwi) {
    PANIC(dw_interface_create() must be called first);
  }
  free(GLOBAL_AUTHORITY);
  curl_easy_cleanup(dwi->curl_handle);
  free(dwi->username);
  free(dwi->password);
  free(dwi);
}

