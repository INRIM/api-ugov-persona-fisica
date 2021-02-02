#!/bin/bash
#if [ -d "$PWD/app/libs" ]; then
#      git -C "$PWD/app/libs" pull
#  else
#      git -C "$PWD/app" clone https://gitlab.ininrim.it/inrimsi/microservices-libs/base-libs.git libs
#fi
docker-compose -f docker-compose.yml stop
docker-compose -f docker-compose.yml -p ugovws-api-pf up  --detach --remove-orphans