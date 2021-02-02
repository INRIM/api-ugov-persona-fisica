#!/bin/bash
docker-compose -f docker-compose.yml stop
docker-compose -f docker-compose.yml up -p ugovWs --detach --remove-orphans