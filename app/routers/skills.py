from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from model import schemas
from controllers.skills import get_skills
from model.database import get_db

from logger import logger

skills_router = APIRouter()

yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()

@skills_router.get("/", response_model=List[schemas.DMSkills])
def read_skills(city:str = 'Москва', profession:str = 'Data engineer', date_from: str = yesterday, date_to: str = yesterday, db: Session = Depends(get_db)):
    logger.info(f"The task of obtaining metrics data is launched.Parameters: city-{city}, profession-{profession}, date_from-{date_from}, date_to-{date_to}.")
    skills = get_skills(db, city, profession, date_from, date_to)
    return skills