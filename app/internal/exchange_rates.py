import requests
from requests.exceptions import ConnectionError
import json
from datetime import datetime, timedelta

from model.core import StgExchangeRates
from model.database import engine
from sqlalchemy.orm import Session

from logger import logger



def run_parse_exchange_rates(date: str | None):
    if date:
        url = f"https://www.cbr-xml-daily.ru/archive/{date}/daily_json.js"
        dt = datetime.strptime(date, "%Y/%m/%d").date()
    else:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        dt = (datetime.now() - timedelta(days=1)).date()
    logger.info("Starting data parsing (%s)", url)
    req = requests.get(url)
    try:
        exchange_rates =  json.loads(req.content.decode(encoding="utf-8"))
        date = dt
        while "error" in exchange_rates:
            logger.error(f"Error, {exchange_rates}")
            date = date - timedelta(days=1)
            url = f"https://www.cbr-xml-daily.ru/archive/{date.strftime('%Y/%m/%d')}/daily_json.js"
            req = requests.get(url)
            exchange_rates =  json.loads(req.content.decode(encoding="utf-8"))
        else:
            logger.info("The process of adding data to the table exchange rates begins.")
            try:
                with Session(autoflush=False, bind=engine) as db:
                    row = StgExchangeRates(obj=exchange_rates, query_dt=dt, update_ts= datetime.now())
                    db.add(row) 
                    db.commit()
                    logger.info("The process of adding data to the exchange rate table has been \
                                completed for the date %s.", dt.strftime('%Y-%m-%d'))
            except ConnectionError as e:
                logger.error("Database unavailable.")
            
    except ConnectionError as e:
        logger.error("No response. %s", e)