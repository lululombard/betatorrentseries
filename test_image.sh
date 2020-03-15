#!/bin/sh
set -e

# Build the docker image
docker build -t betatorrentseries .

mkdir -p downloads

docker run -v downloads:/root/downloads -p 9091:9091 --name betatorrentseries betatorrentseries