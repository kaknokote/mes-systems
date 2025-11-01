# app/models.py
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class SimulationRequest(BaseModel):
    """
    Модель запроса для запуска симуляции
    
    Attributes:
        server_capacity: Количество серверов в системе (должно быть положительным)
        model_name: Название модели в AnyLogic Cloud
        experiment_name: Название эксперимента для запуска
    """
    server_capacity: int = Field(
        ..., 
        gt=0, 
        description="Количество серверов (должно быть > 0)"
    )
    model_name: str = Field(
        default="Service System Demo", 
        description="Название модели"
    )
    experiment_name: str = Field(
        default="Simulation", 
        description="Название эксперимента"
    )
    
    class Config:
        # Пример данных для документации Swagger
        json_schema_extra = {
            "example": {
                "server_capacity": 5,
                "model_name": "Service System Demo",
                "experiment_name": "Simulation"
            }
        }


class SimulationResponse(BaseModel):
    """
    Модель ответа с результатами симуляции
    
    Attributes:
        simulation_id: Уникальный ID симуляции в AnyLogic Cloud
        server_capacity: Использованное количество серверов
        mean_queue_size: Средний размер очереди (результат симуляции)
        server_utilization: Загрузка серверов в процентах
        raw_outputs: Все сырые данные из AnyLogic
        status: Статус выполнения симуляции
        timestamp: Время выполнения симуляции
    """
    simulation_id: str
    server_capacity: int
    mean_queue_size: float
    server_utilization: float
    raw_outputs: Dict[str, Any]
    status: str
    timestamp: Optional[datetime] = None


class ModelInfo(BaseModel):
    """
    Информация о модели в AnyLogic Cloud
    
    Attributes:
        id: Уникальный идентификатор модели
        name: Название модели
        latest_version_id: ID последней версии модели
    """
    id: str
    name: str
    latest_version_id: Optional[str] = None
    version_name: Optional[str] = None
    version_number: Optional[int] = None


class ErrorResponse(BaseModel):
    """
    Модель ответа при ошибке
    
    Attributes:
        detail: Описание ошибки
        status_code: HTTP код ошибки
    """
    detail: str
    status_code: int
