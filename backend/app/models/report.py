from pydantic import BaseModel
from typing import Optional


class ReportResponse(BaseModel):
    id: str
    file_name: str
    file_type: str
    uploaded_at: str
    analysis: Optional[str] = None