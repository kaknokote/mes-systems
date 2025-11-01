import os
from anylogiccloudclient.client.cloud_client import CloudClient
from fastapi import HTTPException

def get_cloud_client():
    """Инициализация клиента AnyLogic Cloud"""
    api_key = os.getenv("ANYLOGIC_API_KEY", "e05a6efa-ea5f-4adf-b090-ae0ca7d16c20")
    try:
        return CloudClient(api_key)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка инициализации клиента AnyLogic: {str(e)}"
        )