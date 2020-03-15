#!/bin/sh
set -e

# Build the docker image
docker build -t betatorrentseries .

docker run betatorrentseries