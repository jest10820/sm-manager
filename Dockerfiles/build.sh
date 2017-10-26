#!/bin/bash

currdir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker build -t="jest10820/sm-pgsql" "$currdir"/postgresql
docker build -t="jest10820/sm-pgadmin" "$currdir"/pgadmin
docker build -t="jest10820/python" "$currdir"/python
docker build -t="jest10820/vue" "$currdir"/vue
docker build -t="jest10820/vue-frontend" "$currdir"/vue-frontend
docker build -t="jest10820/nginx" "$currdir"/nginx
docker build -t="jest10820/sm-backend" "$currdir"/backend
docker build -t="jest10820/sm-backend-dev" --file "$currdir"/backend/Dockerfile-dev "$currdir"/backend
