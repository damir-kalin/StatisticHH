from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from model import schemas
from controllers.metrics import get_metrics
from model.database import get_db
from logger import logger

metrics_router = APIRouter()

yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()

@metrics_router.get("/", response_model=List[schemas.DMMetrics])
def read_metrics(city:str = 'Москва', profession:str = 'Data engineer', date_from: str = yesterday, date_to: str = yesterday, db: Session = Depends(get_db)):
    logger.info(f"The task of obtaining skills data is launched.Parameters: city-{city}, profession-{profession}, date_from-{date_from}, date_to-{date_to}.")
    metrics = get_metrics(db, city, profession, date_from, date_to)
    return metrics