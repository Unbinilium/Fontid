#!/bin/bash

#Require root permission
if [ "$(id -u)" != 0 ]; then
    sudo bash "$0"
    exit 1
fi

#Pushd to docker directory
pushd "$(dirname $0)"

#Copy source files
cp -r '../src' '.'

#Build docker image
docker build -t font-identifier-rest-api .

#Cleanup
rm -fr 'src'
popd
