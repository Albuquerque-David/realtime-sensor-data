from datetime import datetime
from utils.auth import create_access_token
import pytest

@pytest.fixture
def valid_token():
    return create_access_token(data={"username": "test_user"})

@pytest.mark.asyncio
async def test_create_sensor_data(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    payload = {
        "equipmentId": "STATION_1",
        "timestamp": datetime.utcnow().isoformat(),
        "value": 25.0,
    }
    response = await client.post("/sensors/data", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["message"] == "Data inserted"

@pytest.mark.asyncio
async def test_upload_csv(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    csv_content = "equipmentId,timestamp,value\nSTATION_1,2024-12-06T12:00:00+00:00,25.0\nSTATION_2,2024-12-06T12:00:00+00:00,30.0"
    files = {"file": ("data.csv", csv_content)}
    response = await client.post("/sensors/upload", files=files, headers=headers)
    assert response.status_code == 202
    assert "inserted_count" in response.json()

@pytest.mark.asyncio
async def test_get_average(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    equipment_id = "STATION_1"
    period = "24h"
    response = await client.get(f"/sensors/average?equipmentId={equipment_id}&period={period}", headers=headers)
    assert response.status_code == 200
    assert "average" in response.json()

@pytest.mark.asyncio
async def test_fetch_average_all_stations(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    period = "24h"
    response = await client.get(f"/sensors/averages?period={period}", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_fetch_station_data(client, valid_token):
    headers = {"Authorization": f"Bearer {valid_token}"}
    equipment_id = "STATION_1"
    period = "24h"
    response = await client.get(f"/sensors/{equipment_id}/data?period={period}", headers=headers)
    assert response.status_code == 200
    assert "values" in response.json()
    assert "average" in response.json()
