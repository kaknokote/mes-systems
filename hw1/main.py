from fastapi import FastAPI, HTTPException
from anylogiccloudclient.client.cloud_client import CloudClient

app = FastAPI()
client = CloudClient("e05a6efa-ea5f-4adf-b090-ae0ca7d16c20")

@app.get("/run-simulation/")
async def run_simulation(server_capacity: int = 8):
    try:
        version = client.get_latest_model_version("Service System Demo")
        inputs = client.create_inputs_from_experiment(version, "Baseline")
        inputs.set_input("Server capacity", server_capacity)
        simulation = client.create_simulation(inputs)
        outputs = simulation.get_outputs_and_run_if_absent()
        mean_queue_size = outputs.value("Mean queue size|Mean queue size")
        server_utilization = outputs.value("Utilization|Server utilization")
        return {
            "server_capacity": server_capacity,
            "mean_queue_size": mean_queue_size,
            "server_utilization": server_utilization,
            "raw_outputs": outputs.get_raw_outputs()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка моделирования: {str(e)}")
