/*
 * This is the config file for the DataWarehouse interface.
 * This file is for preprocessor macros for easy updates.
 * This file is for internal use only.
 */

/* Constants */

// IP address for the EC2 instance.
#define REMOTE_IP_ADDR "44.204.92.26"

// IP address for localhost.
#define LOCAL_IP_ADDR  "127.0.0.1"

// Different ports for different databases.
// 5000 -> Development (aka dw_dev)
// 4000 -> Staging     (aka dw_staging)
// 3000 -> Production  (aka dw_prod)
#define DEVELOPMENT_PORT ":5000"
#define STAGING_PORT     ":4000"
#define PRODUCTION_PORT  ":3000"

// Paths for different controllers.
#define HANDSHAKE_PATH "/api/prepare/"
#define INSERT_PATH    "/api/store/"
#define QUERY_PATH     "/api/query/"

// Enable or disable this macro in order to print verbose steps
// in datawarehouse_interface.c. Intended for debugging purposes.
#define VERBOSE

/* Libraries */

#include <assert.h> // Debugging. Should not be in release.
#include <errno.h>  // Error handling.
#include <regex.h>  // For verifying UUIDS are correct based off of regular expression.
#include <stdio.h>  // I/O.
#include <stdlib.h> // Standard library.
#include <string.h> // Functions for string manipulation.

// NOTE: To install (Linux): sudo apt install libcurl4-openssl-dev
// NOTE: To install (MacOS): brew install curl
// NOTE: Library documentation: https://curl.se/libcurl/c/
#include <curl/curl.h> // Communication with the DataWarehouse.
