from config.database import db
from utils.csv_parser import parse_csv
from datetime import datetime, timedelta
from fastapi import HTTPException, UploadFile, status
import logging

logger = logging.getLogger("SensorDataAPI")

async def insert_sensor_data(sensor):
    """
    Inserts individual sensor data into the database.

    Parameters:
    - sensor (SensorData): Object containing sensor data:
        - equipmentId (str): Unique identifier of the equipment.
        - timestamp (datetime): Date and time of the event.
        - value (float): Sensor value.

    Returns:
    - dict: Success message and ID of the inserted record.

    Raises:
    - HTTPException (500): If an error occurs while inserting the data.
    """
    try:
        result = await db["sensors"].insert_one(sensor.dict())
        logger.info(f"Data inserted for equipmentId {sensor.equipmentId}.")
        return {"message": "Data inserted", "id": str(result.inserted_id)}
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

async def process_csv_upload(file: UploadFile):
    """
    Processes a CSV file and inserts the data into the database.

    Parameters:
    - file (UploadFile): CSV file uploaded by the client.

    Returns:
    - dict: Success message and the number of records inserted.

    Raises:
    - HTTPException (400): If the CSV has an invalid format.
    - HTTPException (500): If an error occurs during processing or insertion.

    Example of CSV format:
    - Columns: equipmentId, timestamp, value
    - Values: EQ-12345, 2024-12-05T15:00:00.000Z, 42.75
    """
    try:
        data = await file.read()
        parsed_data = parse_csv(data)
        if not parsed_data:
            logger.warning("Invalid CSV format received.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid CSV format."
            )
        
        result = await db["sensors"].insert_many(parsed_data)
        logger.info(f"CSV processed successfully. Inserted {len(result.inserted_ids)} records.")
        return {"message": "CSV processed", "inserted_count": len(result.inserted_ids)}
    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

async def calculate_average(equipmentId: str, period: str):
    """
    Calculates the average values of a sensor within a specific period.

    Parameters:
    - equipmentId (str): Unique identifier of the equipment.
    - period (str): Time interval. Accepted values:
        - "24h": Last 24 hours.
        - "48h": Last 48 hours.
        - "1w": Last week.
        - "1m": Last month.

    Returns:
    - dict: Average values for the specified equipment and period:
        - equipmentId (str): Identifier of the equipment.
        - average (float or None): Calculated average or `None` if no data exists.

    Raises:
    - HTTPException (400): If the provided period is invalid.
    - HTTPException (500): If an error occurs during the query or calculation.
    """
    try:
        now = datetime.utcnow()
        period_mapping = {
            "24h": now - timedelta(hours=24),
            "48h": now - timedelta(hours=48),
            "1w": now - timedelta(weeks=1),
            "1m": now - timedelta(days=30),
        }

        if period not in period_mapping:
            logger.warning(f"Invalid period: {period}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid period. Use '24h', '48h', '1w', or '1m'."
            )

        start_time = period_mapping[period]
        cursor = db["sensors"].find({"equipmentId": equipmentId, "timestamp": {"$gte": start_time}})
        values = [doc["value"] async for doc in cursor]

        if not values:
            logger.info(f"No data found for equipmentId {equipmentId} in period {period}.")
            return {"equipmentId": equipmentId, "average": None}

        average = sum(values) / len(values)
        logger.info(f"Average calculated for equipmentId {equipmentId} in period {period}: {average}")
        return {"equipmentId": equipmentId, "average": average}
    except Exception as e:
        logger.error(f"Error calculating average: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

async def get_average_all_stations(period: str):
    """
    Calculates the average values for all stations within the specified period.

    Parameters:
    - period (str): Time interval (24h, 48h, 1w, 1m).

    Returns:
    - list[dict]: A list of dictionaries containing equipmentId and the average.

    Raises:
    - HTTPException (400): If the provided period is invalid.
    - HTTPException (500): If an error occurs during the query.
    """
    try:
        now = datetime.utcnow()
        period_mapping = {
            "24h": now - timedelta(hours=24),
            "48h": now - timedelta(hours=48),
            "1w": now - timedelta(weeks=1),
            "1m": now - timedelta(days=30),
        }

        if period not in period_mapping:
            logger.warning(f"Invalid period: {period}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid period. Use '24h', '48h', '1w', or '1m'."
            )

        start_time = period_mapping[period]

        pipeline = [
            {"$match": {"timestamp": {"$gte": start_time}}},
            {"$group": {"_id": "$equipmentId", "average": {"$avg": "$value"}}},
        ]
        cursor = db["sensors"].aggregate(pipeline)
        results = [{"equipmentId": doc["_id"], "average": doc["average"]} async for doc in cursor]
        logger.info(f"Fetched average data for {len(results)} stations.")
        return results
    except Exception as e:
        logger.error(f"Error fetching station averages: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )

async def get_station_data(equipmentId: str, period: str):
    """
    Fetches all values and the average for a specific station within a period.

    Parameters:
    - equipmentId (str): Station ID.
    - period (str): Time interval (24h, 48h, 1w, 1m).

    Returns:
    - dict: Individual data and average for the station.
    """
    try:
        now = datetime.utcnow()
        period_mapping = {
            "24h": now - timedelta(hours=24),
            "48h": now - timedelta(hours=48),
            "1w": now - timedelta(weeks=1),
            "1m": now - timedelta(days=30),
        }

        if period not in period_mapping:
            logger.warning(f"Invalid period: {period}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid period. Use '24h', '48h', '1w', or '1m'."
            )

        start_time = period_mapping[period]

        # Busca todos os valores da estação
        cursor = db["sensors"].find(
            {"equipmentId": equipmentId, "timestamp": {"$gte": start_time}},
            {"_id": 0, "timestamp": 1, "value": 1}
        )
        values = [doc async for doc in cursor]

        # Calcula a média
        average = sum([v["value"] for v in values]) / len(values) if values else None

        return {"equipmentId": equipmentId, "average": average, "values": values}
    except Exception as e:
        logger.error(f"Error fetching station data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error."
        )


