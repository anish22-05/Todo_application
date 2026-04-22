import os
from pathlib import Path
from dotenv import load_dotenv
from openai import AsyncOpenAI

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from . import models, services, schemas
from .routers import tasks
# Import MasterAgent
from .agent.analytical_agent import MasterAgent
#------------Confermation & Environment-------------------------
#Locate the .env file in the root directory 
basedir = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(basedir,'.env'))
# Initialize the Async OpenAI client
# It automatically looks for OPENAI_API_KEY in your environment
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Distributed Todo Intelligence API", version = "1.0")
app.include_router(tasks.router)
# Initialize the Master Agent once at startup
Agent_master = MasterAgent(api_key=os.getenv("OPENAI_API_KEY"))
@app.get('/')
def root():
    return {"message":"Todo Api is Online."}

# Add the gloabl Context Route 
@app.get("/context")
async def get_current_context(lat: float, lon: float):
    # This endpoint is called by the web app to get location and weather before creating a task.
    return await services.fetch_context_data(lat,lon)
#-----The Agentic Endpoint-------
@app.get("/intelligence",response_model = schemas.IntelligenceResponse)
async def get_task_intelligence(lat: float, lon: float, use_llm: bool= False,db: Session = Depends(get_db)):
    """This acts as brain of api it combines live weatehr, tasks history, and ai agents."""
    context = await services.fetch_context_data(lat,lon)
    # weather = context.get("weather_condition","Clear")
    # location = context.get("location_name", "Unknown")
    # local_time = context.get("local_time_str","Unknown Time")

    # Get all tasks from the DB using sqlalchemy
    db_tasks = db.query(models.Task).all()
    # Run the Agentic Analysis
    report = await Agent_master.run(db_tasks,context_data = context, use_llm = use_llm)
    return {
        "location": context.get("location_name","unknown"),
        "weather": context.get("weather_condition","Clear"),
        "local_time": context.get("local_time_str","Unknown Time"), 
        "temperature": context.get("temperature"),
        "local_date": context.get("local_date"),
        "intelligence_report": report
    }
# @app.get("/")
# def root():
#     return {"message": "Todo API running"}
