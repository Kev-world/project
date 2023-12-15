from typing import Optional
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from databases.sqlDB import engine
from models import model
from routers import auth, project, task

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(project.router)
app.include_router(task.router)