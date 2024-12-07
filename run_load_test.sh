#!/bin/bash

set -e

mkdir -p reports

docker-compose up -d --build

sleep 10

locust -f backend/load_test.py --headless --host=http://localhost:8000 --users 500 --spawn-rate 100 --run-time 1m --csv=reports/results_500
locust -f backend/load_test.py --headless --host=http://localhost:8000 --users 1000 --spawn-rate 200 --run-time 1m --csv=reports/results_1000
locust -f backend/load_test.py --headless --host=http://localhost:8000 --users 5000 --spawn-rate 500 --run-time 1m --csv=reports/results_5000
locust -f backend/load_test.py --headless --host=http://localhost:8000 --users 10000 --spawn-rate 1000 --run-time 1m --csv=reports/results_10000

docker-compose down