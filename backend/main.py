from fastapi import FastAPI, Depends
from middlewares.auth_middleware import get_current_user
from fastapi.middleware.cors import CORSMiddleware
from config.database import initialize_db
from routers.sensors import router as sensors_router
from routers.auth import auth_router as auth_router
from logs.logger import get_logger

logger = get_logger("RealtimeSensorDataAPI")

app = FastAPI(
    title="Sensor Data API",
    description="""
    API para gerenciamento de dados de sensores em tempo real.
    Inclui endpoints para:
    - Inserir dados de sensores.
    - Fazer upload de dados em lote via CSV.
    - Calcular a média dos dados em períodos específicos.
    - Autenticação e registro de usuário.
    """,
    version="1.0.0",
    contact={
        "name": "David Albuquerque",
        "email": "albuquerque.r.david@gmail.com",
    },
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(sensors_router, dependencies=[Depends(get_current_user)])
logger.info("Routes added.")

initialize_db()
logger.info("MongoDB initialized.")

@app.get("/", summary="API Root")
async def root():
    logger.info("Root endpoint accessed.")
    return {"message": "Welcome to the Realtime Sensor Data API"}
