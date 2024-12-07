from fastapi import APIRouter, Query, UploadFile, File, status
from services.sensors_service import (
    insert_sensor_data,
    process_csv_upload,
    calculate_average,
    get_average_all_stations,
    get_station_data
)
from models.sensor_data import SensorData

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.post("/data", status_code=status.HTTP_201_CREATED, summary="Insert Sensor Data", description="Insert individual sensor data into the database.")
async def create_sensor_data(sensor: SensorData):
    """
    Inserts sensor data.

    - **equipmentId**: Unique identifier of the equipment.
    - **timestamp**: Date and time of the event (including timezone).
    - **value**: Sensor value with precision up to two decimal places.
    """
    return await insert_sensor_data(sensor)

@router.post("/upload", status_code=status.HTTP_202_ACCEPTED, summary="Upload Sensor Data CSV", description="Uploads a CSV file containing sensor data for batch insertion.")
async def upload_csv(file: UploadFile = File(...)):
    """
    Processes and inserts sensor data from a CSV file.

    - The CSV must contain the following fields: `equipmentId`, `timestamp`, `value`.
    """
    return await process_csv_upload(file)

@router.get("/average", status_code=status.HTTP_200_OK, summary="Calculate Sensor Data Average", description="Calculates the average values of a sensor over a specific period.")
async def get_average(equipmentId: str, period: str = Query("24h", description="Time interval (24h, 48h, 1w, 1m)")):
    """
    Calculates the average values of a sensor over a defined period.

    - **equipmentId**: Unique identifier of the equipment.
    - **period**: Time interval (accepted values: `24h`, `48h`, `1w`, `1m`).
    """
    return await calculate_average(equipmentId, period)

@router.get("/averages", summary="Get Average Data for All Stations")
async def fetch_average_all_stations(period: str = Query("24h", description="Time interval (24h, 48h, 1w, 1m)")):
    """
    Returns the average data of all stations for the specified time interval.
    """
    return await get_average_all_stations(period)

@router.get("/{equipmentId}/data", summary="Get Data for a Station")
async def fetch_station_data(
    equipmentId: str,
    period: str = Query("24h", description="Time interval (24h, 48h, 1w, 1m)")
):
    """
    Returns the collected values and the average of a station for the specified interval.
    """
    return await get_station_data(equipmentId, period)

