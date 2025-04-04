#!/bin/bash

nginx_id=$(docker ps -q -f name=nginx)

for id in $(docker ps -q)
do
	if [ "$id" != "$nginx_id" ]; then
		docker restart $id
	fi
done

docker restart $nginx_id
