from sqlalchemy import Column,Integer,String, Boolean, DateTime
from sqlalchemy.sql import func
from datetime import datetime
# import uuid
from .database import Base

class Task(Base):
    __tablename__ =  "tasks"
    id = Column(Integer, primary_key=True,index=True)
    title = Column(String, nullable=True)
    priority = Column(String, default="Medium")
    category = Column(String, default="Errand")
    duration = Column(String, default = 20)
    # deadline = Column(DateTime, nullable=True) # i need to add this new column
    location = Column(String,default="Local")
    date = Column(DateTime, default= datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    weather = Column(String)
    completed = Column(Boolean,default=False)
    sync_status= Column(String, default="pending")