#!/bin/bash
read -p "Are you sure? [y/N]" -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Yy]$ ]]
then
docker rm -fv ugovws-api-pf_ugovws-pf
docker rmi python3.8.ugovws
fi