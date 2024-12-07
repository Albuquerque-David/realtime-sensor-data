import requests
import random
import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# Configurações
BACKEND_URL = "http://localhost:8000/sensors/data"
NUM_STATIONS = 2000
INTERVAL = 2
MAX_WORKERS = 100

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
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {station_name} Enviado: {data}")
        else:
            print(f"[{datetime.now().strftime('%H:%M:%S')}] {station_name} Falha ({response.status_code}): {response.text}")
    except requests.RequestException as e:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {station_name} Erro ao enviar: {e}")

def simulate_stations():
    station_names = [f"STATION_{i}" for i in range(1, NUM_STATIONS + 1)]

    print(f"Simulando dados para {NUM_STATIONS} estações...")

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        while True:
            executor.map(send_data, station_names)
            print(f"Esperando {INTERVAL} segundos para o próximo envio...")
            time.sleep(INTERVAL)

simulate_stations()
