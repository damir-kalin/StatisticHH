from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from logger import logger

from model import schemas
from controllers.pipline import run
from model.database import get_db

pipline_router = APIRouter()

yesterday = str((datetime.now() - timedelta(days=1)).date())

@pipline_router.post("/")
def run_pipline(dt: str = yesterday, db: Session = Depends(get_db)):
    logger.info('Data processing task started.')
    dt = datetime.strptime(dt, '%Y-%m-%d').date()
    logger.info(dt)
    run(dt, db)
    
