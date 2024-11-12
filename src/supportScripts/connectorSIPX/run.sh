#!/bin/bash

docker build --tag connector-sipx .
docker run -d -p 8000:8000 connector-sipx

pause
