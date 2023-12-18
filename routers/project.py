from fastapi import APIRouter, Depends, HTTPException, Path, status
from annotated_types import Annotated
from databases.sqlDB import SessionLocal
from sqlalchemy.orm import Session
from dtos.projectDto import CreateProjectDto, UpdateProjectParticipantDto
from .auth import get_current_user
from models.model import Projects

router = APIRouter(
    prefix='/projects',
    tags=[
        'projects'
    ]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get('/')
async def get_all(db: db_dependency, user: user_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Projects).filter(Projects.owner_id == user.get('id')).all()

@router.get('/projects/{id}')
async def get_one(user: user_dependency, db: db_dependency, id: str = Path(min_length=36, max_length=36)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    proj_model = db.query(Projects).filter(Projects.id == id).filter(Projects.owner_id == user.get('id')).first()
    if (proj_model):
        return proj_model
    raise HTTPException(status_code=404, detail='Project Not Found')
    
@router.post('/')
async def create(user: user_dependency, db: db_dependency, dto: CreateProjectDto):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    proj_model = Projects(**dto.model_dump(), owner_id=user.get('id'))

    db.add(proj_model)
    db.commit()

@router.put('/add_participants/{id}')
async def add_participant(user: user_dependency, db: db_dependency, updateDto: UpdateProjectParticipantDto, id: str = Path(min_length=36, max_length=36)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    project_model = db.query(Projects).filter(Projects.id == id).first()
    if project_model is None:
        raise HTTPException(status_code=404, detail='Project Not Found.')
    
    if project_model.participants is None:
        project_model.participants = []

    current_participants_count = len(project_model.participants)
    max_participants = 10
    available_slots = max_participants - current_participants_count

    if available_slots <= 0:
        raise HTTPException(status_code=400, detail='Participants limit reached.')
    
    for part in updateDto.participants:
        if part not in project_model.participants and available_slots > 0:
            project_model.participants.append(part)
            available_slots += 1
        
    db.add(project_model)
    db.commit()