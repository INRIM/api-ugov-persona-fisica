#!/bin/bash
docker stop ugovws
docker container rm ugovws
docker build -t python3.8.ugovws .
docker run --env WEB_CONCURRENCY=3 --restart always -d --name ugovws -p 8022:80 -v $(pwd)/app:/app python3.8.ugovws /start.sh