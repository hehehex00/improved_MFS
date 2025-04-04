#!/bin/bash

CONTAINER_TOTAL=10
CONTAINER_TOTAL=10
CURRENT=0

docker network create nginx-network

echo created nginx-network

cd /data/streamlit-1.0 || exit

####
echo "building toolbox -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach toolbox

echo "building diarization -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach diarization

echo "building diarization_api -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach diarization_api

echo "building hijri_calendar_converter -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach hijri_calendar_converter

echo "building hijri_calendar_converter_api -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach hijri_calendar_converter_api

echo "building text_extractor -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach text_extractor

echo "building image_to_text -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach image_to_text

echo "building arab_dialect_id -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach arab_dialect_id

echo "building cem_search -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach cem_search

echo "building image_triage -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach image_triage

echo "building cure -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach cure

echo "building cure_api -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach cure_api

echo "building translation-api -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach translation-api

echo "building mongrel_api -> Build Progress:$((++CURRENT))/$CONTAINER_TOTAL"
docker compose up --build --detach mongrel_api

echo "restarting reverse proxy"
nginx_id=$(docker ps -q -f name=nginx)
docker restart $nginx_id

echo FIN
