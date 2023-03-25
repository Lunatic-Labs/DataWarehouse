#include "datawarehouse_interface.h"
#include "_datawarehouse_config_INTERNAL.h"

// The `authority` is the part of the url that is: http://ip_addr:port/
char *GLOBAL_AUTHORITY;

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
#ifdef VERBOSE
  printf("Allocated %zu bytes\n", nbytes);
#endif
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
#ifdef VERBOSE
  printf("Reallocated %zu bytes\n", nbytes);
#endif
  return p;
}

/* fopen() wrapper. This function will open a file that is specified with
 * the appropriate permission ("r", "w", "b", "wr", etc.). Error checking is
 * then performed. Returns a pointer to the opened file.
 */
static FILE *open_file(const char *filepath, const char *permission) {
  FILE *fp = fopen(filepath, permission);
  if (!fp) {
    fprintf(stderr, "ERROR: could not open file: %s. Reason: %s\n", filepath, strerror(errno));
    PANIC(Stopping communication with DataWarehouse);
  }
#ifdef VERBOSE
  printf("Opened file: %s with permissions: %s\n", filepath, permission);
#endif
  return fp;
}

/*
 * verify_uuid: A function that checks if a string is a valid UUID.
 * Parameters:
 *   uuid: The string to be checked.
 * Returns:
 *   0 if the string is a valid UUID, REG_NOMATCH if it is not, or a
 *   nonzero error code if an error occurs.
 */
static int verify_uuid(const char *uuid) {
  regex_t regex;
  regcomp(&regex,
          "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
          REG_EXTENDED | REG_NOSUB | REG_ICASE);
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
static struct buffer_t buffer_t_create(size_t m) {
  struct buffer_t buff;
  buff.data = s_malloc(m * sizeof(char));
  buff.size = 0;
  buff.max  = m;
#ifdef VERBOSE
  printf("Created buffer with max size: %zu\n", m);
#endif
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
      PANIC(Invalid environment);
  }

#ifdef VERBOSE
  printf("Set IP address: %s\n", ip_addr);
#endif

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
      PANIC(Invalid port);
  }

#ifdef VERBOSE
  printf("Set port: %s\n", port);
#endif

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

#ifdef VERBOSE
  printf("GLOBAL_AUTHORY = %s\n", GLOBAL_AUTHORITY);
#endif
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

#ifdef VERBOSE
  printf("Constructed URL: %s\n", url);
#endif

  return url;
}

static char *copy_buffer_data(const char *buf_data, size_t buf_sz) {
  char *response = s_malloc(buf_sz + 1);
  strncpy(response, buf_data, buf_sz);
  response[buf_sz] = '\0';

#ifdef VERBOSE
  printf("Copied buffer data\n");
#endif

  return response;
}

static void perform_curl_and_check(CURLcode code) {
  if (code != CURLE_OK) {
    fprintf(stderr, "ERROR: curl_easy_perform() failed. Reason: %s\n",
            curl_easy_strerror(code));
    PANIC();
  }

#ifdef VERBOSE
  printf("CURL performed successfully\n");
#endif
}

// Perform a POST request.
static char *POST_request(const DWInterface *dwi, const char *url, FILE *json_file) {
  char *file_data            = NULL;
  struct curl_slist *headers = NULL;
  size_t file_size;

#ifdef VERBOSE
  printf("Performing POST request with URL: %s\n", url);
#endif

  // Set the url and POST option.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_URL,  url);
  curl_easy_setopt(dwi->curl_handle, CURLOPT_POST, 1L);

  // Set the content type header to application/json.
  headers = curl_slist_append(headers, "Content-Type: application/json");
  curl_easy_setopt(dwi->curl_handle, CURLOPT_HTTPHEADER, headers);

  // Get the size of the file.
  fseek(json_file, 0, SEEK_END);
  file_size = ftell(json_file);
  rewind(json_file);

#ifdef VERBOSE
  printf("Got file size: %zu\n", file_size);
#endif

  // Get the file data.
  file_data = s_malloc(file_size + 1);
  if (!fread(file_data, 1, file_size, json_file)) {
    fprintf(stderr, "ERROR: Failed to read file contents. Reason: %s\n",
            strerror(errno));
    PANIC();
  }
  file_data[file_size] = '\0';

#ifdef VERBOSE
  printf("Got file data\n");
#endif

  struct buffer_t buf = buffer_t_create(1024);

  // Set options for writing data.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_WRITEFUNCTION, callback);
  curl_easy_setopt(dwi->curl_handle, CURLOPT_WRITEDATA,     &buf);

  // Set the request body to the file contents.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_POSTFIELDS, file_data);

  // Set the request body size to the size of the file.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_POSTFIELDSIZE, file_size);

#ifdef VERBOSE
  printf("Performing CURL...\n");
#endif

  // Perform CURL and check for failure.
  perform_curl_and_check(curl_easy_perform(dwi->curl_handle));

  // Copy the buffer data into response.
  char *response = copy_buffer_data(buf.data, buf.size);

  curl_slist_free_all(headers);
  free(buf.data);
  free(file_data);
  return response;
}

// Perform a GET request.
static char *GET_request(const DWInterface *dwi, const char *url) {

#ifdef VERBOSE
  printf("Performing GET request...\n");
#endif

  struct buffer_t buf = buffer_t_create(1024);

  // Set the options for curl.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_WRITEFUNCTION, callback);
  curl_easy_setopt(dwi->curl_handle, CURLOPT_WRITEDATA,     &buf);
  curl_easy_setopt(dwi->curl_handle, CURLOPT_URL,           url);

  // Allow redirects.
  curl_easy_setopt(dwi->curl_handle, CURLOPT_FOLLOWLOCATION, 1L);

#ifdef VERBOSE
  printf("Performing CURL...\n");
#endif
  // Perform CURL and check for failure.
  perform_curl_and_check(curl_easy_perform(dwi->curl_handle));

  // Copy the buffer data into response.
  char *response = copy_buffer_data(buf.data, buf.size);

  free(buf.data);
  return response;
}

Group *dw_interface_group_create(char *classification, char *group_name) {
  Group *group          = s_malloc(sizeof(Group));
  group->classification = classification;
  group->group_name     = group_name;
  group->sources        = NULL;
  group->sources_len    = 0;
  group->sources_cap    = 1;
  return group;
}

Source *dw_interface_source_create(char *name) {
  Source *source       = s_malloc(sizeof(Source));
  source->name         = name;
  source->metrics      = NULL;
  source->metrics_len  = 0;
  source->metrics_cap  = 1;
  return source;
}

Metric *dw_interface_metric_create(int asc, Datatype data_type, char *name, char *units) {
  Metric *metric    = s_malloc(sizeof(Metric));
  metric->asc       = asc;
  metric->data_type = data_type;
  metric->name      = name;
  metric->units     = units;
  return metric;
}

void dw_interface_push_source(Group *group, Source *source) {
  NOP(group);
  NOP(source);
  UNIMPLEMENTED;
}

void dw_interface_push_metric(Group *group, Metric *metric) {
  NOP(group);
  NOP(metric);
  UNIMPLEMENTED;
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
DWInterface *dw_interface_create(char *username,
                                 char *password,
                                 enum ENV env,
                                 enum PORT port) {
  if (!strlen(username) || !strlen(password)) {
    PANIC(Username and password length must be at least 1);
  }

  DWInterface *dwi = s_malloc(sizeof(DWInterface));

  dwi->username = username;
  dwi->password = password;

#ifdef VERBOSE
  printf("Set username: %s and password: %s\n", username, password);
#endif

  // Init curl/curl.h library.
  curl_global_init(CURL_GLOBAL_ALL);

  // Create curl.
  dwi->curl_handle = curl_easy_init();

  dwi->env  = env;
  dwi->port = port;

  // Set all UUIDs blank.
  dwi->uuids[0][0] = '\0';
  dwi->uuids[1][0] = '\0';
  dwi->uuids[2][0] = '\0';

  dwi->groups = NULL;
  dwi->groups_len = 0;
  dwi->groups_cap = 1;

#ifdef VERBOSE
  printf("Building GLOBAL_AUTHORITY...\n");
#endif

  // Build the GLOBAL_AUTHORITY.
  build_GLOBAL_AUTHORITY(dwi);

  return dwi;
}

void dw_interface_set_groups(DWInterface *dwi, Group *groups) {
  dwi->groups = groups;
}

void dw_interface_set_uuids(DWInterface *dwi,
                            const char group_uuid[UUID_LEN],
                            const char source_uuid[UUID_LEN],
                            const char metric_uuid[UUID_LEN]) {
#ifdef VERBOSE
  printf("Verifying UUIDs:\n\t%s\n\t%s\n\t%s\n", group_uuid, source_uuid, metric_uuid);
#endif

  if (verify_uuid(group_uuid) != 0) {
    PANIC(Invalid group_uuid);
  }
  if (verify_uuid(source_uuid) != 0) {
    PANIC(Invalid source_uuid);
  }
  if (verify_uuid(metric_uuid) != 0) {
    PANIC(Invalid metric_uuid);
  }

#ifdef VERBOSE
  printf("Copying UUIDs\n");
#endif

  // Copy UUIDs into DWInterface instance.
  strcpy(dwi->uuids[GROUP_UUID],  group_uuid);
  strcpy(dwi->uuids[SOURCE_UUID], source_uuid);
  strcpy(dwi->uuids[METRIC_UUID], metric_uuid);
}

/*
 * This function takes a JSON file to upload to the DataWarehouse and prints the
 * output into a file called: handshake_information.json. This function should
 * be called before any data insertion or query operations.
 * If `out_filepath` is given, it will also write the data recieved to that file.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that contains information about the
 *        current session.
 *   json_file: a pointer to a FILE object that represents the JSON file.
 *   out_filepath: The file in which to write the data to. Can be NULL.
 * Return value:
 *   None.
 */
char *dw_interface_commit_handshake(const DWInterface *dwi,
                                    const char *handshake_json_filepath,
                                    const char *out_filepath) {
#ifdef VERBOSE
  printf("Performing handshake request with file(s):\n");
  printf("\t%s\n\t%s\n", handshake_json_filepath, out_filepath? out_filepath : "NULL");
#endif

  FILE *infp = open_file(handshake_json_filepath, "r");
  FILE *outfp;

  // This needs to be here in order to not perform the CURL request.
  if (out_filepath) {
    outfp = open_file(out_filepath, "w");
  }

  // Construct a valid url with the GLOBAL_AUTHORITY and the HANDSHAKE_PATH.
  char *url = construct_url(HANDSHAKE_PATH);

  // Perform a POST request.
  char *response = POST_request(dwi, url, infp);

  // Write the received information to an output file.
  if (out_filepath) {
#ifdef VERBOSE
    printf("Writing to file: %s\n", out_filepath);
#endif
    fputs(response, outfp);
    fclose(outfp);
  }

  fclose(infp);
  free(url);

  return response;
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
 */
void dw_interface_insert_data(const DWInterface *dwi, const char *insert_json_filepath) {

#ifdef VERBOSE
  printf("Performing insert data with file: %s\n", insert_json_filepath);
#endif

  FILE *infp = open_file(insert_json_filepath, "r");

  // Construct a valid url with the GLOBAL_AUTHORITY and the INSERT_PATH.
  char *url = construct_url(INSERT_PATH);

  // Perform a POST request.
  POST_request(dwi, url, infp);

  fclose(infp);
  free(url);
}

/*
 * This function sends a query string to the DataWarehouse and returns a JSON
 * formatted string as a result. If `out_filepath` is given, it will also
 * write the data recieved to that file.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that contains information about
 *        the DataWarehouse connection.
 *   query_string: a pointer to a char array that contains the query string.
 *   out_filepath: The file in which to write the data to. Can be NULL.
 * Return value:
 *   A pointer to a char array that contains the JSON formatted string
 *   returned by the DataWarehouse.
 */
char *dw_interface_query_data(const DWInterface *dwi,
                              const char *query_string,
                              const char *out_filepath) {
#ifdef VERBOSE
  printf("Performing query data with query string and (file):\n");
  printf("\t%s\n\t%s\n", query_string, out_filepath? out_filepath : "NULL");
#endif

  UUIDS_PRESENT(dwi);
  FILE *outfp;

  // This needs to be here in order to not perform the CURL request.
  if (out_filepath) {
    outfp = open_file(out_filepath, "w");
  }

  if (*(query_string) != '?') {
    PANIC(Invalid query string. The first character of a query_string must be '?');
  }

  // Construct a valid url with the GLOBAL_AUTHORITY and the QUERY_PATH.
  char *url = construct_url(QUERY_PATH);

  // Get lengths of all necessary strings to build the appropriate url.
  size_t query_string_len = strlen(query_string);
  size_t group_uuid_len   = strlen(dwi->uuids[GROUP_UUID]);
  size_t source_uuid_len  = strlen(dwi->uuids[SOURCE_UUID]);
  size_t url_len          = strlen(url);

  // + 1 for '/' and + 1 for '/' and +1 for '\0'.
  char *url_uuids_query_string //         /                                        /  \0
    = s_malloc(url_len + group_uuid_len + 1 + source_uuid_len + query_string_len + 1 + 1);

  // Start concatenating the strings together to build the final url.
  strncpy(url_uuids_query_string, url, url_len);
  strncat(url_uuids_query_string, dwi->uuids[GROUP_UUID], group_uuid_len);
  strcat(url_uuids_query_string, "/");
  strncat(url_uuids_query_string, dwi->uuids[SOURCE_UUID], source_uuid_len);
  strcat(url_uuids_query_string, "/");
  strncat(url_uuids_query_string, query_string, query_string_len);
  // url_uuids_query_string should now look like: http://ip_addr:port/group_uuid/source_uuid/query_string

#ifdef VERBOSE
  printf("Built url_uuids_query_string: %s\n", url_uuids_query_string);
#endif

  char *response = GET_request(dwi, url_uuids_query_string);

  // Write the received information to an output file.
  if (out_filepath) {
#ifdef VERBOSE
    printf("Writing to file: %s\n", out_filepath);
#endif
    fputs(response, outfp);
    fclose(outfp);
  }

  free(url);
  free(url_uuids_query_string);
  return response;
}

/*
 * This function frees up all the memory allocated by the DWInterface struct and its fields.
 * Parameters:
 *   dwi: a pointer to a DWInterface struct that needs to be destroyed.
 */
void dw_interface_destroy(DWInterface *dwi) {
  if (!dwi) {
    PANIC(dw_interface_create() must be called first);
  }
#ifdef VERBOSE
  printf("Destroying DWInterface...\n");
#endif
  free(GLOBAL_AUTHORITY);
  curl_easy_cleanup(dwi->curl_handle);

  // Free all groups, sources, and metrics.
  for (size_t i = 0; i < dwi->groups_len; i++) {
    for (size_t j = 0; j < dwi->groups[i].sources_len; j++) {
      for (size_t k = 0; k < dwi->groups[i].sources[j].metrics_len; k++) {
	free(dwi->groups[i].sources[j].metrics);
      }
      free(dwi->groups[i].sources);
    }
    free(dwi->groups);
  }
  free(dwi);
}
