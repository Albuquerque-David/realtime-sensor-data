#!/bin/bash

echo "[REALTIME-SENSOR-DATA] Inicializando o deploy das aplicações..."

docker-compose up --build -d

echo "[REALTIME-SENSOR-DATA] Serviços iniciados com sucesso!"