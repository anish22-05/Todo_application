"""This code will take care of quries to database that will help inserting and updating the database.
Since we have to use already completed and stored records so we wont be hard deleting the db records."""
from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas

# Create: we will be saving all info we get from our application interface
def create_task(db:Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump()) # This **task.model_dump() it will unpack 
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task
# -------------------------------This part is for later use ----------------------------------------
# # Read: this function will get tasks that are not completed
# def get_acitve_tasks(db:Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Task).filter(models.Task.completed= False).offset(skip).limit(limit).all()
# # Read this read would be for agent 
# def get_all_tasks_history():
#     pass
# # Read to get a single task
# def get_task_by_id(db:Session,task_id:int):
#     return db.query(models.Task).filter(models.Task.id == task_id).first()
# # Update if we need to update tasks in middle
# Read Gets list of all tasks (acitve and completed)
def get_all_tasks(db:Session):
    return db.query(models.Task).all()
# UPDATE: Change specific details of a task.
def update_task(db:Session,task_id:int,task_update:schemas.TaskUpdate):
    # Find the task present in db which we want to update. this acts as select query to db here models.Task is table name, .filter acts as where clause.
    db_task = db.query(models.Task).filter(models.Task.id== task_id).first() #.first() returns the first occurence of the id record.
    if db_task:
        # Get only the fields the user actually sent for update, we use exclude_unset=True which ignore all other fields which do not
        # require any change (None) and change only those fileds which have values other than None.
        update_data = task_update.model_dump(exclude_unset=True)
        # Loop through and update those fields
        for key, value in update_data.items():
            setattr(db_task,key,value)
        db.commit()
        db.refresh(db_task)
    return db_task

# Archive: just flip the completed switch to True
def archive_task(db:Session,task_id:int):
    db_task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if db_task:
        db_task.completed = True
        db_task.completed_at = datetime.utcnow()
        db_task.sync_status = "pending"
        db.commit()
        db.refresh(db_task)
    return db_task


