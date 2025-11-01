# app/routers/simulations.py
from fastapi import APIRouter, HTTPException, Depends, Query, Path
from typing import List
from app.dependencies import MockCloudClient as CloudClient
import logging
from datetime import datetime

# Импорт наших моделей и зависимостей
from app.models import SimulationRequest, SimulationResponse, ErrorResponse, ModelInfo
from app.dependencies import get_cloud_client

# Настройка логирования с форматированием
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание роутера с настройками
router = APIRouter(
    prefix="/simulations",  # Все пути будут начинаться с /simulations
    tags=["simulations"],   # Группировка в Swagger UI
    responses={404: {"description": "Не найдено"}}
)


@router.post(
    "/run",
    response_model=SimulationResponse,
    summary="Запуск симуляции",
    description="""
    Запускает симуляцию демо-модели Service System Demo с заданными параметрами.
    
    **Параметры:**
    - server_capacity: Количество серверов в системе (целое число > 0)
    - model_name: Название модели для запуска
    - experiment_name: Название эксперимента
    
    **Возвращает:**
    - Результаты симуляции включая средний размер очереди и загрузку серверов
    """,
    response_description="Результаты выполненной симуляции",
    status_code=200,
    responses={
        200: {"description": "Симуляция успешно выполнена"},
        400: {"description": "Неверные входные данные"},
        500: {"model": ErrorResponse, "description": "Ошибка сервера"}
    }
)
async def run_simulation(
    request: SimulationRequest,
    client: CloudClient = Depends(get_cloud_client)
) -> SimulationResponse:
    """
    Основной эндпоинт для запуска симуляций в AnyLogic Cloud.
    
    **Процесс выполнения:**
    1. Получение информации о модели из AnyLogic Cloud
    2. Настройка параметров симуляции
    3. Запуск симуляции
    4. Получение и обработка результатов
    5. Возврат результатов клиенту
    
    Args:
        request: Параметры симуляции (валидируются автоматически)
        client: Клиент AnyLogic Cloud (внедряется через Depends)
        
    Returns:
        SimulationResponse: Объект с результатами симуляции
        
    Raises:
        HTTPException 400: Если параметры запроса некорректны
        HTTPException 500: Если произошла ошибка при выполнении симуляции
    """
    # Логируем начало операции
    logger.info(
        f"Запуск симуляции для модели '{request.model_name}' "
        f"с {request.server_capacity} серверами"
    )
    
    try:
        # ========== ДОПОЛНИТЕЛЬНАЯ ВАЛИДАЦИЯ ==========
        if request.server_capacity <= 0:
            logger.warning(f"Попытка запуска с некорректным server_capacity: {request.server_capacity}")
            raise HTTPException(
                status_code=400,
                detail="Количество серверов должно быть положительным числом"
            )
        
        # ========== ШАГ 1: Получение версии модели ==========
        logger.info(f"Получение версии модели '{request.model_name}'")
        version = client.get_latest_model_version(request.model_name)
        logger.info(f"Найдена версия модели: {version.id}")
        
        # ========== ШАГ 2: Создание входных параметров ==========
        logger.info(f"Создание параметров для эксперимента '{request.experiment_name}'")
        inputs = client.create_inputs_from_experiment(version, request.experiment_name)
        
        # ========== ШАГ 3: Установка пользовательских параметров ==========
        logger.info(f"Установка server_capacity = {request.server_capacity}")
        inputs.set_input("Server capacity", request.server_capacity)
        
        # ========== ШАГ 4: Создание и запуск симуляции ==========
        logger.info("Создание симуляции...")
        simulation = client.create_simulation(inputs)
        logger.info(f"Симуляция создана с ID: {simulation.id}")
        
        # ========== ШАГ 5: Получение результатов ==========
        logger.info("Ожидание результатов симуляции...")
        outputs = simulation.get_outputs_and_run_if_absent()
        logger.info("Результаты получены")
        
        # ========== ШАГ 6: Извлечение конкретных показателей ==========
        mean_queue_size = outputs.value("Mean queue size|Mean queue size")
        server_utilization = outputs.value("Utilization|Server utilization")
        
        logger.info(
            f"Результаты: средний размер очереди = {mean_queue_size:.2f}, "
            f"загрузка серверов = {server_utilization:.2f}%"
        )
        
        # ========== ШАГ 7: Формирование и возврат ответа ==========
        return SimulationResponse(
            simulation_id=simulation.id,
            server_capacity=request.server_capacity,
            mean_queue_size=mean_queue_size,
            server_utilization=server_utilization,
            raw_outputs=outputs.get_raw_outputs(),
            status="completed",
            timestamp=datetime.now()
        )
        
    except HTTPException:
        # Перевыбрасываем HTTP исключения без изменений
        raise
        
    except Exception as e:
        # Логируем полную информацию об ошибке
        logger.error(f"Ошибка при выполнении симуляции: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Внутренняя ошибка при выполнении симуляции: {str(e)}"
        )


@router.get(
    "/models",
    response_model=List[ModelInfo],
    summary="Получить список моделей",
    description="Возвращает список всех доступных моделей в AnyLogic Cloud",
    responses={
        200: {"description": "Список моделей успешно получен"},
        500: {"description": "Ошибка при получении списка моделей"}
    }
)
async def get_models(
    client: CloudClient = Depends(get_cloud_client),
    include_versions: bool = Query(
        False, 
        description="Включать подробную информацию о версиях моделей"
    )
) -> List[ModelInfo]:
    """
    Получение списка всех доступных моделей в AnyLogic Cloud.
    
    **Query параметры:**
    - include_versions: Если True, добавляет информацию о версиях моделей
    
    Args:
        client: Клиент AnyLogic Cloud (внедряется автоматически)
        include_versions: Флаг для включения информации о версиях
        
    Returns:
        List[ModelInfo]: Список объектов с информацией о моделях
        
    Raises:
        HTTPException 500: Если не удалось получить список моделей
    """
    try:
        logger.info("Запрос списка моделей из AnyLogic Cloud")
        
        # Получаем список моделей от клиента
        models = client.get_models()
        result = []
        
        # Обрабатываем каждую модель
        for model in models:
            # Базовая информация о модели
            model_info = ModelInfo(
                id=model.id,
                name=model.name,
                latest_version_id=model.latest_version.id if model.latest_version else None
            )
            
            # Добавляем дополнительную информацию о версиях если запрошено
            if include_versions and model.latest_version:
                model_info.version_name = model.latest_version.name
                model_info.version_number = model.latest_version.number
            
            result.append(model_info)
        
        logger.info(f"Возвращено {len(result)} моделей")
        return result
        
    except Exception as e:
        logger.error(f"Ошибка получения списка моделей: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Не удалось получить список моделей: {str(e)}"
        )


@router.get(
    "/models/{model_id}",
    response_model=ModelInfo,
    summary="Получить информацию о модели",
    description="Возвращает подробную информацию о конкретной модели по ID",
    responses={
        200: {"description": "Информация о модели получена"},
        404: {"description": "Модель не найдена"},
        500: {"description": "Ошибка сервера"}
    }
)
async def get_model_by_id(
    model_id: str = Path(..., description="Уникальный идентификатор модели"),
    client: CloudClient = Depends(get_cloud_client)
) -> ModelInfo:
    """
    Получение подробной информации о конкретной модели по её ID.
    
    **Path параметры:**
    - model_id: Уникальный идентификатор модели в AnyLogic Cloud
    
    Args:
        model_id: ID модели (берется из URL пути)
        client: Клиент AnyLogic Cloud
        
    Returns:
        ModelInfo: Информация о найденной модели
        
    Raises:
        HTTPException 404: Если модель с указанным ID не найдена
        HTTPException 500: Если произошла ошибка при поиске
    """
    try:
        logger.info(f"Поиск модели с ID: {model_id}")
        
        # Получаем все модели
        models = client.get_models()
        
        # Ищем модель по ID
        for model in models:
            if model.id == model_id:
                logger.info(f"Модель найдена: {model.name}")
                return ModelInfo(
                    id=model.id,
                    name=model.name,
                    latest_version_id=model.latest_version.id if model.latest_version else None,
                    version_name=model.latest_version.name if model.latest_version else None,
                    version_number=model.latest_version.number if model.latest_version else None
                )
        
        # Если модель не найдена
        logger.warning(f"Модель с ID {model_id} не найдена")
        raise HTTPException(
            status_code=404,
            detail=f"Модель с ID {model_id} не найдена"
        )
        
    except HTTPException:
        raise
        
    except Exception as e:
        logger.error(f"Ошибка при поиске модели {model_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при поиске модели: {str(e)}"
        )


# Дополнительный эндпоинт для проверки здоровья API
@router.get(
    "/health",
    summary="Проверка работоспособности",
    description="Проверяет, что API работает корректно",
    tags=["health"]
)
async def health_check():
    """
    Простой эндпоинт для проверки работоспособности API.
    
    Returns:
        dict: Статус API и время сервера
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "AnyLogic Simulation API"
    }
