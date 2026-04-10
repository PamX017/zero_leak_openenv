import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any

# Adjust imports based on your directory structure. 
from models import ZeroLeakAction, ZeroLeakObservation, ZeroLeakState
from server.my_env_environment import ZeroLeakEnv

app = FastAPI(title="Zero-Leak OpenEnv Server", version="1.0.0")

# Initialize our stateful environment engine
env_instance = ZeroLeakEnv()

# ------------------------------------------------------------------------
# RESPONSE MODELS
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
    return {"status": "ok", "environment": "Zero-Leak Engineering Assistant"}

@app.post("/reset", response_model=ZeroLeakObservation)
async def reset_env():
    try:
        return await env_instance.reset()
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
# THE FIX: MULTI-MODE DEPLOYMENT BLOCK (Required by Meta Validator)
# =========================================================================
def main():
    """
    This function satisfies the strict 'multi-mode deployment' check.
    It allows the Scaler automated evaluator to run the server directly.
    """
    uvicorn.run(app, host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()