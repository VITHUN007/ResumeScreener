from typing import List, Union
from pydantic import BaseModel

class ResumeSchema(BaseModel):
    name: str
    skills: List[str]
    years_of_experience: int
    summary: str
    relevance_score: int
    reasoning: str