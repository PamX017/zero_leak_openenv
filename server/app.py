import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Ensure models and environment are imported correctly from your structure
from models import ZeroLeakAction, ZeroLeakObservation, ZeroLeakState
from server.my_env_environment import ZeroLeakEnv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI(title="Zero-Leak OpenEnv Server", version="1.0.0")

# Mount static files for the custom dashboard
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize our stateful environment engine
env_instance = ZeroLeakEnv()

# ------------------------------------------------------------------------
# RESPONSE MODELS: Required for Pydantic serialization
# ------------------------------------------------------------------------
class StepResponse(BaseModel):
    observation: ZeroLeakObservation
    reward: float
    done: bool
    info: Dict[str, Any]

class ResetRequest(BaseModel):
    task_id: Optional[str] = None

# ------------------------------------------------------------------------
# API ENDPOINTS: Standard OpenEnv Spec
# ------------------------------------------------------------------------
@app.get("/")
async def health_check():
    """MANDATORY: Used by the validator to check if server is live."""
    return {"status": "ok", "environment": "Zero-Leak Engineering Assistant"}

@app.get("/web")
async def serve_ui():
    """Serves the custom Red-Teaming Dashboard."""
    return FileResponse("static/index.html")

@app.post("/reset", response_model=ZeroLeakObservation)
async def reset_env(request: Optional[ResetRequest] = None):
    try:
        task_id = request.task_id if request else None
        return await env_instance.reset(task_id=task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

@app.post("/step", response_model=StepResponse)
async def step_env(action: ZeroLeakAction):
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
    try:
        return await env_instance.state()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"State retrieval failed: {str(e)}")

# =========================================================================
# THE FIX: MULTI-MODE DEPLOYMENT BLOCK
# Satisfies: server/app.py missing main() function
# Satisfies: server/app.py main() function not callable
# =========================================================================
def main():
    """
    This function satisfies the strict 'multi-mode deployment' check.
    It allows the Scaler automated evaluator to run the server programmatically.
    """
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
    