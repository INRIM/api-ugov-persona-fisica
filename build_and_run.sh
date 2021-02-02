#!/bin/bash
docker-compose -f docker-compose.yml stop
docker-compose -f docker-compose.yml -p ugovWs up  --detach --remove-orphans