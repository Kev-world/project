from databases.sqlDB import Base
from sqlalchemy import ARRAY, Column, ForeignKey, Integer, String, Boolean, Date

class Projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(100))
    date_created = Column(Date)
    owner_id = Column(String(100))

class Tasks(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(100))
    date_created = Column(Date)
    priority = Column(Integer)
    is_completed = Column(Boolean, default=False)
    assigned_to = Column(String(100), default="")
    project_id = Column(Integer, ForeignKey('projects.id'))