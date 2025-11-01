# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Импортируем наш роутер
from app.routers import simulations

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создание экземпляра FastAPI приложения
app = FastAPI(
    title="AnyLogic Simulation API",
    description="""
    API для запуска и управления симуляциями в AnyLogic Cloud.
    
    ## Возможности:
    * **Запуск симуляций** - запуск моделей с пользовательскими параметрами
    * **Получение списка моделей** - просмотр доступных моделей
    * **Получение информации о модели** - детальная информация о конкретной модели
    
    ## Как использовать:
    1. Получите список доступных моделей через `/simulations/models`
    2. Запустите симуляцию через `/simulations/run` с нужными параметрами
    3. Получите результаты в ответе
    """,
    version="1.0.0",
    docs_url="/docs",  # Swagger UI будет доступен по адресу /docs
    redoc_url="/redoc"  # ReDoc будет доступен по адресу /redoc
)

# Настройка CORS (Cross-Origin Resource Sharing)
# Позволяет фронтенду с другого домена обращаться к API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все HTTP методы
    allow_headers=["*"],  # Разрешить все заголовки
)

# Подключение роутера к приложению
# Все эндпоинты из simulations.router будут доступны с префиксом /api/v1
app.include_router(
    simulations.router,
    prefix="/api/v1",  # Версионирование API
    tags=["simulations"]
)


# Корневой эндпоинт - приветственное сообщение
@app.get("/", tags=["root"])
async def root():
    """
    Корневой эндпоинт API.
    
    Returns:
        dict: Приветственное сообщение и ссылки на документацию
    """
    return {
        "message": "Добро пожаловать в AnyLogic Simulation API!",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/api/v1/simulations/health"
    }


# Событие запуска приложения
@app.on_event("startup")
async def startup_event():
    """
    Выполняется при запуске приложения.
    Можно использовать для инициализации подключений к БД и т.д.
    """
    logger.info("=" * 50)
    logger.info("Запуск AnyLogic Simulation API")
    logger.info("Документация доступна по адресу: http://localhost:8000/docs")
    logger.info("=" * 50)


# Событие остановки приложения
@app.on_event("shutdown")
async def shutdown_event():
    """
    Выполняется при остановке приложения.
    Можно использовать для закрытия подключений.
    """
    logger.info("Остановка AnyLogic Simulation API")
