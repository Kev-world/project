from typing import List
from pydantic import BaseModel, Field
from datetime import datetime

class CreateProjectDto(BaseModel):
    title: str = Field(min_length=5)
    description: str = Field(min_length=5, max_length=100)
    date_created: datetime = None

class UpdateProjectParticipantDto(BaseModel):
    participants:List[str]