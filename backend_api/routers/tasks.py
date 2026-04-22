from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..database import get_db
from .. import services 

router = APIRouter(
    prefix="/tasks",
    tags = ["Tasks"],
    redirect_slashes=True
)
@router.post("", response_model=schemas.TaskResponse)
def create_new_task(task:schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db,task)
@router.get("",response_model= List[schemas.TaskResponse])
def read_active_tasks(db:Session=Depends(get_db)):
    # This calls our simplified get_all_tasks from crud.py
    return crud.get_all_tasks(db)
# Arochive Route: we dont want to delete the db records as tasks complete
@router.patch("/{task_id}/complete",response_model=schemas.TaskResponse)
def complete_task(task_id: int, db:Session = Depends(get_db)):
    db_task = crud.archive_task(db,task_id=task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail = "Task not found")
    return db_task
@router.patch("/{task_id}/update",response_model=schemas.TaskResponse)
def update_existing_task(task_id: int, task:schemas.TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id, task)
    if not db_task:
        raise HTTPException(status_code = 404, detail= "Task not found")
    return db_task

# @router.get("/context")
# async def get_current_context(lat: float, lon: float):
#     try:
#         data = await services.fetch_context_data(lat,lon)
#         return data
#     except Exception as e:
#         raise HTTPException(status_code=500, detail = "Failed to fetch context")

