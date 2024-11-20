from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session
from sqlalchemy import text

from model.core import DCity
from model.core import DQueryProfession
from internal.parse import run_parse_vacancies
from internal.exchange_rates import run_parse_exchange_rates
from logger import logger

YESTARDAY = (datetime.now() - timedelta(days=1)).date()
COUNT_PAGE = 3
PER_PAGE = 100

def run(dt: date, db: Session):
    is_full = True
    logger.info("Pipline started.")
    cities = db.query(DCity).all()
    professions = db.query(DQueryProfession).all()
    dates = []
    if dt != YESTARDAY:
        while dt <= YESTARDAY:
            dates.append(dt)
            dt = dt + timedelta(days= 1)
    else:
        dates.append(YESTARDAY)
        is_full = False
    logger.info(dates)
    for dt in dates:
        run_parse_exchange_rates(dt.strftime('%Y/%m/%d'))
        for city in cities:
            for profession in professions:
                for page in range(COUNT_PAGE):
                    logger.info(f"Parse vacancies started with parameters: date - {dt}, city - {city.name}, \
                                profession - {profession.eng_name}, page - {page}")
                    count_row = run_parse_vacancies(profession.eng_name, dt.strftime('%Y-%m-%d'), page, PER_PAGE, city.id)
                    logger.info(f"The process of adding data to the table vacancy is complete. \
                                Added {count_row} lines. Parsing of vacancies completed.")
                    if count_row == 0:
                        break
    try:
        if is_full:
            db.execute(text('call full_pipline();'))
        else:
            db.execute(text('call increment_pipline();'))
    except RuntimeError('The procedure for adding metrics was not completed.') as exc:
        logger.error('The procedure for adding metrics was not completed.')
        raise RuntimeError('Failed to run procedure') from exc
    else:
        db.commit()     