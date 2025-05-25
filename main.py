from fastapi import FastAPI, HTTPException, status
from db.database import DatabaseManager
from db.models import PassData
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Конфигурация БД из переменных окружения
db_config = {
    'dbname': os.getenv('DB_NAME', 'mountain_passes'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', ''),
    'host': os.getenv('DB_HOST', 'localhost')
}

db_manager = DatabaseManager(db_config)


@app.post("/submitData/", status_code=status.HTTP_201_CREATED)
async def submit_data(pass_data: PassData):
    result = db_manager.add_pass(pass_data.dict())

    if result['status'] == 200:
        return {"status": result['status'], "message": result['message'], "id": result['id']}
    elif result['status'] == 400:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": 400, "message": result['message'], "id": None}
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": 500, "message": result['message'], "id": None}
        )


@app.on_event("shutdown")
async def shutdown_event():
    db_manager.close()