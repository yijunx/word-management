from typing import Any, Optional
from pydantic import BaseModel


class StandardResponse(BaseModel):
    success: bool
    response: Any
    message: Optional[str]

    # well here is the error_code needed???
    # well i am not sure..
    error_code: Optional[int]
