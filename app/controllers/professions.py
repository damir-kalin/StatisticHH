from sqlalchemy.orm import Session

from model.core import DQueryProfession
from logger import logger

def get_professions(db: Session):
    logger.info("Data with professions is generated.")
    try:
        professions = db.query(DQueryProfession).all()
        logger.info("Mission accomplished.")
        return professions
    except ConnectionAbortedError as e:
        logger.error("Connection error %s", e)