from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from model.core import DMSkills
from logger import logger

yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()

def get_skills(db: Session, city:str = 'Москва', profession: str = 'Data engineer', date_from: str = yesterday, date_to: str = yesterday):
    logger.info("Data with skills is generated.")
    try:
        metrics = (db.query(DMSkills)
                .filter((DMSkills.city_name == city)
                        & (DMSkills.query_profession_eng_name == profession)
                        & (DMSkills.dt >= date_from)
                        & (DMSkills.dt <= date_to)
                        )
                        .all())
        logger.info("Mission accomplished.")
        return metrics
    except ConnectionAbortedError as e:
        logger.error("Connection error %s", e)