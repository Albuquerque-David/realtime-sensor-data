import argparse
import random
import requests
import time
from datetime import datetime

BACKEND_URL = "http://localhost:8000/sensors/data"
INTERVAL = 2

def generate_value():
    return round(random.uniform(20.0, 30.0), 2)

def send_data(station_name):
    value = generate_value()
    timestamp = datetime.utcnow().isoformat() + "Z"

    data = {
        "equipmentId": station_name,
        "timestamp": timestamp,
        "value": value,
    }

    try:
        response = requests.post(BACKEND_URL, json=data)
        if response.status_code == 201:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Enviado: {data}")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Falha ({response.status_code}): {response.text}")
    except requests.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Erro ao enviar: {e}")

def main():
    parser = argparse.ArgumentParser(description="Simula uma estação enviando dados para o backend.")
    parser.add_argument(
        "station_name",
        type=str,
        help="Nome da estação (equipmentId) a ser simulada.",
    )
    args = parser.parse_args()

    station_name = args.station_name
    print(f"Simulando dados da estação '{station_name}' para {BACKEND_URL}...\n")
    
    while True:
        send_data(station_name)
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
