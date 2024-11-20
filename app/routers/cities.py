from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from model import schemas
from controllers.cities import get_cities
from model.database import get_db
from logger import logger

cities_router = APIRouter()

@cities_router.get("/", response_model=List[schemas.DCities])
def read_cities(db: Session = Depends(get_db)):
    logger.info(f"The task of obtaining cities data is launched.")
    cities = get_cities(db)
    return cities 