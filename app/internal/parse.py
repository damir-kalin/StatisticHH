from datetime import datetime, date, timedelta
import requests
from requests.exceptions import ConnectionError
import json

from sqlalchemy.orm import Session

from model.core import StgVacancies
from model.database import engine
from logger import logger

# page - номер первой страницы
# cnt_page - количество страниц
# per_page - количество элементов на сранице
# text - переданное значение ищется в полях вакансии
# areas - регион, город

URL = 'https://api.hh.ru/vacancies'

def run_parse_vacancies(text:str, dt:str, page:int =0, per_page:int =100, area:int =113):
    parameters = {'text': text, 'date_from': dt, 'date_to': dt, 'area':area, 'per_page':per_page, 'page':page}
    req = requests.get(URL, params=parameters)
    try:
        i = 0
        data = json.loads(req.content.decode(encoding='utf-8'))#['items']
        if "errors" not in data:
            for vacancy in data['items']:
                req_vacancy = requests.get(vacancy['url'])
                value = json.loads(req_vacancy.content.decode(encoding='utf-8'))
                if "errors" not in value:
                    i += 1
                    try:
                        with Session(autoflush=False, bind=engine) as db:
                            row = StgVacancies(obj=value, query_profession_eng_name=text, query_dt=dt, update_ts= datetime.now())
                            db.add(row) 
                            db.commit()
                    except ConnectionError as e:
                        logger.error("Database unavailable.")
                    logger.info("Added row %s.", i)
        return i
    except ConnectionError as e:
        logger.error("No response. %s", e)