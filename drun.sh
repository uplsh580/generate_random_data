#!/bin/bash

TAG="grd"
VERSION="1.0.0"
CNAME="grd"

RM_IMAGE=$(docker images "${TAG}:${VERSION}" -q)

case "$1" in
    --clean) # clean docker image and container
        docker container rm -f $CNAME
        docker image rm -f $RM_IMAGE
        exit 0
        ;;
    --run) # create docker image and run container
    docker build --tag ${TAG}:${VERSION} .
    docker container run --name ${CNAME} \
        -v $(pwd):/app \
        -it ${TAG}:${VERSION} \
        /bin/bash
    exit 0
        ;;
    -h|--help)
        echo "Usage:  $0 -i <input> [options]" >&2
        echo "        --clean     (clean docker container and image)" >&2
        echo "        --run       (build image and run docker container)" >&2
        exit 0
        ;;
    -*|--*) # unsupported flags
        echo "Error: Unsupported flag: $1" >&2
        echo "$0 -h for help message" >&2
        exit 1
        ;;
    *)
        echo "Error: Arguments with not proper flag: $1" >&2
        echo "$0 -h for help message" >&2
        exit 1
        ;;
esac
# done
