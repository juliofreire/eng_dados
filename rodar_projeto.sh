#!/bin/bash

docker compose up -d

sleep 15

curl -X POST -H "Content-Type: application/json" --data @mongo-connectors.json http://localhost:8083/connectors

docker exec -it kafka kafka-console-consumer --bootstrap-server kafka:9092 --topic topic.db_eng_dados.acoes --from-beginning > arquivo.txt