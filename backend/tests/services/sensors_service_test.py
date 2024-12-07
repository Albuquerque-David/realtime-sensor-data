import pytest
from datetime import datetime, timedelta
from models.sensor_data import SensorData
from services.sensors_service import (
    insert_sensor_data,
    calculate_average,
    get_average_all_stations,
    get_station_data
)
import services.sensors_service

@pytest.fixture
def sample_data():
    return [
        {"equipmentId": "STATION_1", "timestamp": datetime.utcnow(), "value": 25.0},
        {"equipmentId": "STATION_1", "timestamp": datetime.utcnow() - timedelta(hours=1), "value": 30.0},
        {"equipmentId": "STATION_2", "timestamp": datetime.utcnow(), "value": 20.0},
    ]

@pytest.mark.asyncio
async def test_insert_sensor_data(mock_db):
    services.sensors_service.db = mock_db
    sensor_data = SensorData(
        equipmentId="STATION_1",
        timestamp=datetime.utcnow(),
        value=25.0
    )
    result = await insert_sensor_data(sensor_data)
    assert result["message"] == "Data inserted"
    assert "id" in result

@pytest.mark.asyncio
async def test_calculate_average(mock_db, sample_data):
    services.sensors_service.db = mock_db
    collection = mock_db["sensors"]
    await collection.insert_many(sample_data)

    result = await calculate_average("STATION_1", "24h")
    assert result["equipmentId"] == "STATION_1"
    assert pytest.approx(result["average"], 0.1) == 27.5

@pytest.mark.asyncio
async def test_get_average_all_stations(mock_db, sample_data):
    services.sensors_service.db = mock_db
    collection = mock_db["sensors"]
    await collection.insert_many(sample_data)

    result = await get_average_all_stations("24h")
    assert len(result) == 2
    assert any(station["equipmentId"] == "STATION_1" for station in result)
    assert any(station["equipmentId"] == "STATION_2" for station in result)
