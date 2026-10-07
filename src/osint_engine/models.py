from typing import Optional, Dict, Any
from pydantic import BaseModel

class ModuleResult(BaseModel):
    module_name: str
    category: str
    target: str
    status: str  # FOUND, NOT_FOUND, ERROR
    details: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None