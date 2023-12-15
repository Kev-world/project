from pydantic import BaseModel, Field
from datetime import datetime

class CreateTaskDto(BaseModel):
    content: str = Field(min_length=5)
    date_created: datetime = None
    priority: int = Field(gt=0, lt=6)
    is_completed: bool
    project_id: str = Field(min_length=36, max_length=36)
    