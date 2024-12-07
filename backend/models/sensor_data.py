from pydantic import BaseModel, Field
from datetime import datetime

class SensorData(BaseModel):
    equipmentId: str
    timestamp: datetime
    value: float

class CSVUploadResponse(BaseModel):
    message: str
    inserted_count: int