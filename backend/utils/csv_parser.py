import csv
from datetime import datetime

def parse_csv(data: bytes):
    try:
        decoded = data.decode("utf-8")
        reader = csv.DictReader(decoded.splitlines())
        result = []
        for row in reader:
            result.append({
                "equipmentId": row["equipmentId"],
                "timestamp": datetime.fromisoformat(row["timestamp"]),
                "value": float(row["value"])
            })
        return result
    except Exception as e:
        print(f"Error parsing CSV: {e}")
        return None
