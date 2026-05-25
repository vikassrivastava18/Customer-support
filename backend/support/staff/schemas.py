from pydantic import BaseModel
from typing import Literal

class IntentSchema(BaseModel):
    intent: Literal["info", "query"]