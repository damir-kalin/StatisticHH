from sqlalchemy.orm import Session

from model.core import DCity
from logger import logger

def get_cities(db: Session):
    logger.info("Data with cities is generated.")
    try:
        cities = db.query(DCity).all()
        logger.info("Mission accomplished.")
        return cities
    except ConnectionAbortedError as e:
        logger.error("Connection error %s", e)