from fastapi import APIRouter, HTTPException, Depends
from anylogiccloudclient.client.cloud_client import CloudClient
import logging

from app.models import SimulationRequest, SimulationResponse, ErrorResponse
from app.dependencies import get_cloud_client

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post(
    "/simulations/run",
    response_model=SimulationResponse,
    responses={500: {"model": ErrorResponse}}
)
async def run_simulation(
    request: SimulationRequest,
    client: CloudClient = Depends(get_cloud_client)
):
    """
    Запуск симуляции демо-модели Service System Demo
    """
    try:
        logger.info(f"Запуск симуляции с параметрами: {request.dict()}")
        
        # Получение последней версии модели
        version = client.get_latest_model_version(request.model_name)
        logger.info(f"Найдена версия модели: {version.id}")
        
        # Создание входных параметров
        inputs = client.create_inputs_from_experiment(version, request.experiment_name)
        
        # Установка параметров
        inputs.set_input("Server capacity", request.server_capacity)
        
        # Создание и запуск симуляции
        simulation = client.create_simulation(inputs)
        logger.info(f"Создана симуляция с ID: {simulation.id}")
        
        # Получение результатов
        outputs = simulation.get_outputs_and_run_if_absent()
        logger.info("Симуляция завершена, получены результаты")
        
        # Извлечение данных
        mean_queue_size = outputs.value("Mean queue size|Mean queue size")
        server_utilization = outputs.value("Utilization|Server utilization")
        
        return SimulationResponse(
            simulation_id=simulation.id,
            server_capacity=request.server_capacity,
            mean_queue_size=mean_queue_size,
            server_utilization=server_utilization,
            raw_outputs=outputs.get_raw_outputs(),
            status="completed"
        )
        
    except Exception as e:
        logger.error(f"Ошибка при выполнении симуляции: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка моделирования: {str(e)}"
        )

@router.get("/models")
async def get_models(client: CloudClient = Depends(get_cloud_client)):
    """
    Получение списка доступных моделей
    """
    try:
        # Получение всех моделей
        models = client.get_models()
        models_list = []
        
        for model in models:
            models_list.append({
                "id": model.id,
                "name": model.name,
                "latest_version_id": model.latest_version.id if model.latest_version else None
            })
        
        return {"models": models_list}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения списка моделей: {str(e)}"
        )