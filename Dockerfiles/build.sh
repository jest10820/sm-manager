#!/bin/bash

docker build -t="jest10820/sm-pgsql" ~/sm-manager/Dockerfiles/postgresql
docker build -t="jest10820/sm-pgadmin" ~/sm-manager/Dockerfiles/pgadmin
