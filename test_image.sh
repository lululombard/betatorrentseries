#!/bin/bash
set -e

cd "${0%/*}"

# Build the docker image
docker build -t betatorrentseries .

mkdir -p downloads

docker run -v `pwd`/downloads:/root/downloads -p 9091:9091 --name betatorrentseries betatorrentseries