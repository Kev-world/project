from databases.sqlDB import Base
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(50))
    description = Column(String(100))
    date_created = Column(Date)
    owner_id = Column(String(100))

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    content = Column(String(100))
    date_created = Column(Date)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    assigned_to = Column(String(100), default="")
    project_id = Column(String(36), ForeignKey('projects.id'))