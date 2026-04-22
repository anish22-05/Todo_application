"""This code will be used to validate api input, defining api responses so that invalid data 
from reaching database. It acts as checker which prevent database 
from crashing with any unwanted input"""
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

class TaskBase(BaseModel):

    title: str
    priority: Optional[str] = "Medium"
    category: Optional[str] = "Errand"
    duration: Optional[int] = 20
    location: Optional[str] = "Local"
    date: Optional[datetime] = None
    created_at: Optional[datetime]= Field(default_factory=datetime.now) 
    weather: Optional[str] = None
    completed: bool = False
    sync_status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    # This inherits everything from TaskBase
    pass

class TaskUpdate(BaseModel):
    # update will not have created_at field 
    title: Optional[str] = None
    priority: Optional[str] = None
    category: Optional[str] = None
    duration: Optional[int] = None
    location: Optional[str]= None
    date: Optional[datetime] = None
    weather: Optional[str] = None
    completed: Optional[bool] = None
    sync_status: Optional[str] = None
class IntelligenceResponse(BaseModel):
    location: str
    weather: str
    local_time: str
    temperature:Optional[float] = None
    local_date: Optional[str] = None
    intelligence_report: str
class TaskResponse(TaskBase):
    id: int # 
    # Since we are inheriting the TaskBase so rest of the variables of TaskBase will be available here too
    # class config:
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)
    
    
