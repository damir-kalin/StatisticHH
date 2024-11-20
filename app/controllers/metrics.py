from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from model.core import DMMetrics
from logger import logger

yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()

def get_metrics(db: Session, city:str = 'Москва', profession: str = 'Data engineer', date_from: str = yesterday, date_to: str = yesterday):
    logger.info("Data with skills is generated.")
    try:
        metrics = (db.query(DMMetrics)
                .filter((DMMetrics.city_name == city)
                        & (DMMetrics.query_profession_eng_name == profession)
                        & (DMMetrics.dt >= date_from)
                        & (DMMetrics.dt <= date_to)
                        )
                        .all())
        logger.info("Mission accomplished.")
        return metrics
    except ConnectionAbortedError as e:
        logger.error("Connection error %s", e)