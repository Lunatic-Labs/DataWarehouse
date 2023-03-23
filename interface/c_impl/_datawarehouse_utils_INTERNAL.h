#include <stdlib.h>
#include <curl/curl.h>

/*
 * This is the utilities file for the DataWarehouse interface.
 * This file is for help during development as well as enums.
 * This file is for internal use only.
 */

// Less confusion when accessing DWInterface->uuids.
#define GROUP_UUID  0
#define SOURCE_UUID 1
#define METRIC_UUID 2

// Length of UUIDs.
#define UUID_LEN 36

/* Development Macros */

// `No Operation`. Use to surpress `unused variable` warnings.
#define NOP(x) (void)(x);

// Put in functions to crash at unimplemented features.
#define UNIMPLEMENTED printf("Unimplemented: %s at line %d\n", __func__, __LINE__); \
  exit(EXIT_FAILURE);

// Check if the UUIDs have been set.
#define UUIDS_PRESENT(dwi)                      \
  do {                                          \
    for (int i = 0; i < 3; i++) {               \
      if (dwi->uuids[i][0] == '\0') {           \
        PANIC(UUIDs must be set);               \
      }                                         \
    }                                           \
  } while (0)

// Our current way of handling errors. This will print an error message and crash.
#define PANIC(msg)                                                      \
  do {                                                                  \
    fprintf(stderr, "Panic: %s at %s:%d\n", #msg, __FILE__, __LINE__);  \
    exit(EXIT_FAILURE);                                                 \
  } while (0)

/* Enumerations */

// Ports. This is to determine which database we will
// be sending information to/from. We will mostly be
// working in PORT_DEV.
enum PORT {
  PORT_DEV,
  PORT_STAGING,
  PORT_PROD,
};

// Environments. Use ENV_LOCAL if the server is
// running locally.
enum ENV {
  ENV_LOCAL,
  ENV_REMOTE
};

// TODO: Instead of calling PANIC() whenever a fatal error occurs, we should
//       eventually move to using error codes and have a better way to handle
//       errors or failures.
enum ErrorCode {
  OK = 1,
};

enum Datatypes {
  TEXT         = 1,
  TUPLETYPE    = 2,
  STRING       = 3,
  INTEGER      = 4,
  SMALLINTEGER = 5,
  BIGINTEGER   = 6,
  NUMERIC      = 7,
  FLOAT        = 8,
  DATETIME     = 9,
  DATE         = 10,
  TIME         = 11,
  LARGEBINARY  = 12,
  BOOLEAN      = 13,
  UNICODE      = 14,
  UNICODETEXT  = 15,
  INTERVAL     = 16,
};

/* Structs */

typedef struct Metric {
  int   asc;
  int   data_type;
  char *name;
  char *units;
} Metric;

typedef struct Source {
  char   *name;
  Metric *metrics; // TODO: Make a dynamic array.
  size_t metrics_len;
  size_t metrics_cap;
} Source;

typedef struct Group {
  char   *classification;
  char   *group_name;
  Source *sources; // TODO: Make a dynamic array.
  size_t sources_len;
  size_t sources_cap;
} Group;

/*
 * DWInterface: A structure that represents a DataWarehouse interface. It contains
 * fields for the username and password of the user, and a curl handle for
 * making HTTP requests to the DataWarehouse server.
 */
typedef struct DWInterface {
  char *username;
  char *password;
  CURL *curl_handle;
  char uuids[3][UUID_LEN + 1];
  Group *groups;
  enum ENV env;
  enum PORT port;
} DWInterface;

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

