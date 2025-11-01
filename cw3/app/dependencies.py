# app/dependencies.py
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


# ========== MOCK КЛАССЫ для демонстрации (вместо реального AnyLogic) ==========

class MockModelVersion:
    """Имитация версии модели AnyLogic"""
    def __init__(self, model_id: str, name: str):
        self.id = f"version_{model_id}"
        self.name = name
        self.number = 1


class MockModel:
    """Имитация модели AnyLogic"""
    def __init__(self, model_id: str, name: str):
        self.id = model_id
        self.name = name
        self.latest_version = MockModelVersion(model_id, name)


class MockInputs:
    """Имитация входных параметров симуляции"""
    def __init__(self):
        self.params = {}
    
    def set_input(self, name: str, value: Any):
        """Установка входного параметра"""
        self.params[name] = value
        logger.info(f"Установлен параметр: {name} = {value}")


class MockOutputs:
    """Имитация выходных результатов симуляции"""
    def __init__(self, server_capacity: int):
        self.server_capacity = server_capacity
        # Простая формула для демонстрации
        self.data = {
            "Mean queue size|Mean queue size": max(0, 10 - server_capacity * 1.5),
            "Utilization|Server utilization": min(100, 50 + server_capacity * 8)
        }
    
    def value(self, key: str) -> float:
        """Получение значения показателя"""
        return self.data.get(key, 0.0)
    
    def get_raw_outputs(self) -> Dict[str, Any]:
        """Получение всех сырых данных"""
        return self.data


class MockSimulation:
    """Имитация симуляции"""
    def __init__(self, simulation_id: str, inputs: MockInputs):
        self.id = simulation_id
        self.inputs = inputs
    
    def get_outputs_and_run_if_absent(self) -> MockOutputs:
        """Запуск симуляции и получение результатов"""
        logger.info(f"Выполнение mock-симуляции {self.id}")
        server_capacity = self.inputs.params.get("Server capacity", 1)
        return MockOutputs(server_capacity)


class MockCloudClient:
    """
    Mock-клиент для демонстрации работы API без реального AnyLogic Cloud.
    Имитирует поведение настоящего CloudClient.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self._simulation_counter = 0
        logger.info("Создан MockCloudClient (демо-режим)")
    
    def get_models(self):
        """Возвращает список демо-моделей"""
        return [
            MockModel("model_1", "Service System Demo"),
            MockModel("model_2", "Manufacturing Line Demo"),
            MockModel("model_3", "Supply Chain Demo"),
        ]
    
    def get_latest_model_version(self, model_name: str):
        """Возвращает последнюю версию модели"""
        logger.info(f"Получение версии модели: {model_name}")
        return MockModelVersion("latest", model_name)
    
    def create_inputs_from_experiment(self, version, experiment_name: str):
        """Создает входные параметры для эксперимента"""
        logger.info(f"Создание параметров для эксперимента: {experiment_name}")
        return MockInputs()
    
    def create_simulation(self, inputs: MockInputs):
        """Создает новую симуляцию"""
        self._simulation_counter += 1
        sim_id = f"sim_{self._simulation_counter:04d}"
        logger.info(f"Создана симуляция: {sim_id}")
        return MockSimulation(sim_id, inputs)


def get_cloud_client() -> MockCloudClient:
    """
    Функция-зависимость для получения клиента.
    В демо-режиме возвращает MockCloudClient.
    
    Returns:
        MockCloudClient: Mock-клиент для демонстрации
    """
    logger.info("Возвращен MockCloudClient (демо-режим)")
    return MockCloudClient(api_key="DEMO_KEY")


def get_current_user():
    """
    Пример дополнительной зависимости для аутентификации.
    """
    return {"username": "demo_user", "role": "admin"}
