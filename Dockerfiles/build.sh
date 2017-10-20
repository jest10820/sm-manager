#!/bin/bash

currdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker build -t="jest10820/sm-pgsql" "$currdir"/postgresql
docker build -t="jest10820/sm-pgadmin" "$currdir"/pgadmin
docker build -t="jest10820/python" "$currdir"/python
docker build -t="jest10820/vue" "$currdir"/vue
docker build -t="jest10820/vue-frontend" "$currdir"/frontend
docker build -t="jest10820/nginx" "$currdir"/nginx
