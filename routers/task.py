from fastapi import APIRouter, Depends, HTTPException, Path
from annotated_types import Annotated
from databases.sqlDB import SessionLocal
from sqlalchemy.orm import Session
from models.model import Tasks, Projects
from routers.auth import get_current_user
from dtos.taskDto import CreateTaskDto, AssignTaskDto

router = APIRouter(
    prefix='/tasks',
    tags=['tasks']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]



@router.get('/{id}')
async def get_one(user: user_dependency, db: db_dependency, id: str = Path(min_length=36, max_length=36)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Tasks).filter(Tasks.id == id).first()

@router.get('/projects/{projectId}')
async def get_all(user: user_dependency, db: db_dependency, projectId: str = Path(min_length=36, max_length=36)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Tasks).filter(Tasks.project_id == projectId).all()

@router.post('/')
async def create(
    user: user_dependency, 
    db: db_dependency, 
    dto: CreateTaskDto,
    ):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    project = db.query(Projects).filter(Projects.id == dto.project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail='Project Not Found')
    task_model = Tasks(**dto.model_dump(), assigned_to=user.get('id'))

    db.add(task_model)
    db.commit()

@router.put('/{taskId}')
async def update_assigned_personel(
    user: user_dependency, 
    db: db_dependency, 
    dto: AssignTaskDto, 
    taskId: str = Path(min_length=36, max_length=36)
    ):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    task = db.query(Tasks).filter(Projects.id == taskId).first()
    if task is None:
        raise HTTPException(status_code=404, detail='Task Not Found')
    
    task.assigned_to = dto.assigned_to

    db.add(task)
    db.commit()