
from pydantic import BaseModel,Field
from datetime import datetime
from typing import Optional

from sqlalchemy import null

class TodoRequest(BaseModel):
    title:str 
    description:str
    status:str
    priority:str
    tags:dict
    due_date: Optional[datetime] = None
    owner_id: Optional[str] = None
    model_config ={
        "json_schema_extra": {
            "example":{
                "status": "pending",
                    "tags": {
                        "type": "work",
                        "urgent": "no"
                    },
                    "due_date": "2025-10-10T10:00:00",
                    "title": "Team meeting",
                    "description": "Prepare presentation for weekly team meeting",
                    "priority": "medium",
                    "owner_id": "U93LLL69X2P"
                }
            }
        } 