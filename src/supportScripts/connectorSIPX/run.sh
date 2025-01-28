#!/bin/bash

docker rm --force connector-sipx

docker build --tag connector-sipx .
docker run -d -p 8000:8000 --name connector-sipx connector-sipx
