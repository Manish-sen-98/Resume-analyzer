from pydantic import BaseModel
from typing import List, Optional

class ResumeData(BaseModel):
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    experience: List[dict] 
    education: List[dict]
    summary: Optional[str] = None  
    ats: int
    job_role: str
    pdf_url: str

    class Config:
        from_attributes = True
