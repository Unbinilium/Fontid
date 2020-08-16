#!/bin/bash

#Pushd to docker directory
BASE_DIR="$(dirname \"$0\")"
pushd ${BASE_DIR}

#Copy required files
mkdir 'app'
cp '../src/server.py' 'app/server.py'
cp '../src/requirements.txt' 'requirements.txt'

#Build docker image
sudo docker build -t font-identifier-restapi .

#Cleanup
rm -fr 'app'
popd
