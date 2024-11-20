from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from model import schemas
from controllers.professions import get_professions
from model.database import get_db
from logger import logger

professions_router = APIRouter()

@professions_router.get("/", response_model=List[schemas.DProfessions])
def read_professions(db: Session = Depends(get_db)):
    logger.info(f"The task of obtaining professions data is launched.")
    professions = get_professions(db)
    return professions 