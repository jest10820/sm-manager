#!/bin/bash

curr_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker run -it --network=dockerfiles_default -v "$curr_dir"/python/app:/usr/src/app -w /usr/src/app jest10820/python bash
