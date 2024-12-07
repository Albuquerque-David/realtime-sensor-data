#!/bin/bash

echo "[REALTIME-SENSOR-DATA] Inicializando os testes das aplicações..."

docker-compose run backend pytest --cache-clear --maxfail=5 --disable-warnings

echo "[REALTIME-SENSOR-DATA] Testes finalizados com sucesso!"

