from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any
from app.pipeline import MailGentPipeline

router=APIRouter()
pipeline=MailGentPipeline()

class EmailIngestRequest(BaseModel):
    subject:str
    sender:str
    email_text:str

@router.post("/ingest")
def ingest_email(payload: EmailIngestRequest):
    return pipeline.run(payload.dict())    