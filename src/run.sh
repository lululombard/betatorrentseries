#!/bin/bash

set -e

if [ $START_TRANSMISSION_DAEMON -eq 1 ]; then
    /usr/bin/transmission-daemon -a "*"
fi

cd "${0%/*}"

python3 betatorrent.py