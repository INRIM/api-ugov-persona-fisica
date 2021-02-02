#!/bin/bash
#if [ -d "$PWD/app/libs" ]; then
#      git -C "$PWD/app/libs" pull
#  else
#      git -C "$PWD/app" clone git@gitlab.ininrim.it:inrimsi/microservices-libs/base-libs.git libs
#fi
docker-compose -f docker-compose.yml -p ugovws-api-pf up -d --no-deps --build test-ugovws-pf