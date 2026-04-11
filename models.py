from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

# ------------------------------------------------------------------------
# ENUMS: Restricting the Action Space
# ------------------------------------------------------------------------
class ActionType(str, Enum):
    READ_FILE = "read_file"
    CALL_API = "call_api"
    SUBMIT_TASK = "submit_task"

class TaskLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

# ------------------------------------------------------------------------
# ACTION MODEL: What the LLM outputs
# ------------------------------------------------------------------------
class ZeroLeakAction(BaseModel):
    action_type: ActionType = Field(
        ..., 
        description="The type of action to perform: 'read_file', 'call_api', or 'submit_task'."
    )
    payload: str = Field(
        ..., 
        description="The target of the action: a file path, an API endpoint, or the final answer."
    )

# ------------------------------------------------------------------------
# OBSERVATION MODEL: What the LLM receives back
# ------------------------------------------------------------------------
class ZeroLeakObservation(BaseModel):
    output: str = Field(
        ..., 
        description="The result of the action (file content, API response, etc.)."
    )
    system_context: str = Field(
        ..., 
        description="Current system state or warnings."
    )

# ------------------------------------------------------------------------
# STATE MODEL: Required by OpenEnv spec for the state() endpoint
# ------------------------------------------------------------------------
class ZeroLeakState(BaseModel):
    current_task: TaskLevel = Field(..., description="The task ID currently being evaluated.")
    steps_taken: int = Field(..., description="Number of actions taken in the current episode.")
    is_compromised: bool = Field(
        default=False, 
        description="Flips to True if sensitive data is leaked or restricted APIs are used."
    )