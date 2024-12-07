#!/bin/bash

echo "[REALTIME-SENSOR-DATA] Reiniciando os serviços..."

docker-compose down
docker-compose up --build -d

echo "[REALTIME-SENSOR-DATA] Serviços reiniciados."
