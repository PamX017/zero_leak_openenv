from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Adjust imports based on your directory structure. 
# Assuming the container runs from the root of the project.
from models import ZeroLeakAction, ZeroLeakObservation, ZeroLeakState
from server.my_env_environment import ZeroLeakEnv

app = FastAPI(title="Zero-Leak OpenEnv Server", version="1.0.0")

# Initialize our stateful environment engine
env_instance = ZeroLeakEnv()

# ------------------------------------------------------------------------
# RESPONSE MODELS: Ensuring strict compliance with OpenEnv expected returns
# ------------------------------------------------------------------------
class StepResponse(BaseModel):
    observation: ZeroLeakObservation
    reward: float
    done: bool
    info: Dict[str, Any]

# ------------------------------------------------------------------------
# API ENDPOINTS
# ------------------------------------------------------------------------
@app.get("/")
async def health_check():
    """
    MANDATORY FOR HF SPACES: 
    The validator and HF Space will ping this to ensure the container is alive (HTTP 200).
    """
    return {"status": "ok", "environment": "Zero-Leak Engineering Assistant"}

@app.post("/reset", response_model=ZeroLeakObservation)
async def reset_env():
    """OpenEnv Spec: Resets the environment for a new episode."""
    try:
        return await env_instance.reset()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.post("/step", response_model=StepResponse)
async def step_env(action: ZeroLeakAction):
    """OpenEnv Spec: Executes an action and returns the new state/reward."""
    try:
        obs, reward, done, info = await env_instance.step(action)
        return StepResponse(
            observation=obs, 
            reward=reward, 
            done=done, 
            info=info
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Step execution failed: {str(e)}")

@app.get("/state", response_model=ZeroLeakState)
async def get_state():
    """OpenEnv Spec: Returns the hidden internal state of the environment."""
    try:
        return await env_instance.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"State retrieval failed: {str(e)}")