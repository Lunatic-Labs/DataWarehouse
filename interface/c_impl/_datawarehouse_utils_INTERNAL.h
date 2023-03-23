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
#define UNIMPLEMENTED  printf("Unimplemented: %s at line %d\n", __func__, __LINE__); \
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

typedef struct Metric {
  int   asc;
  int   data_type;
  char *name;
  char *units;
} Metric;

typedef struct Source {
  char   *name;
  Metric *metrics;
} Source;

typedef struct Group {
  char   *classification;
  char   *group_name;
  Source *sources;
} Group;


