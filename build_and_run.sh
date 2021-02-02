#!/bin/bash
docker-compose -f docker-compose.yml stop
docker-compose -f docker-compose.yml -p ugovws up  --detach --remove-orphans