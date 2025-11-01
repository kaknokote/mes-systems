from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from app.routers import simulations

# Загрузка переменных окружения
load_dotenv()

# Создание приложения FastAPI
app = FastAPI(
    title="AnyLogic Cloud API Integration",
    description="FastAPI приложение для работы с AnyLogic Cloud",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(simulations.router, prefix="/api/v1", tags=["simulations"])

@app.get("/")
async def root():
    return {"message": "AnyLogic Cloud API Integration Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}