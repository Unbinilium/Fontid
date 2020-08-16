#!/bin/bash

#Pushd to docker directory
pushd "$(dirname $0)"

#Copy required files
mkdir 'app'
cp '../src/server.py' 'app/server.py'
cp '../src/requirements.txt' 'requirements.txt'

#Build docker image
sudo docker build -t font-identifier-restapi .

#Cleanup
rm -fr 'app' 'requirements.txt'
popd
