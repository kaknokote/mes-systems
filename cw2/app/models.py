from pydantic import BaseModel
from typing import Dict, Any, Optional

class SimulationRequest(BaseModel):
    server_capacity: int = 8
    model_name: str = "Service System Demo"
    experiment_name: str = "Baseline"

class SimulationResponse(BaseModel):
    simulation_id: str
    server_capacity: int
    mean_queue_size: float
    server_utilization: float
    raw_outputs: Dict[str, Any]
    status: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None