#!/bin/bash

currdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker build -t="jest10820/sm-pgsql" "$currdir"/postgresql
docker build -t="jest10820/sm-pgadmin" "$currdir"/pgadmin
docker build -t="jest10820/python" "$currdir"/python
