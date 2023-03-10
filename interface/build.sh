#!/bin/bash
set -x
gcc -lcurl -o main main.c datawarehouse_interface.c
