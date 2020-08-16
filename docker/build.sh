#!/bin/bash

#Require root permission
if [ "$(id -u)" != 0 ]; then
    sudo bash "$0"
    exit 1
fi

#Pushd to docker directory
pushd "$(dirname $0)"

#Copy required files
mkdir 'app'
cp '../src/server.py' 'app/server.py'
cp '../src/requirements.txt' 'requirements.txt'

#Build docker image
docker build -t font-identifier-rest-api .

#Cleanup
rm -fr 'app' 'requirements.txt'
popd
