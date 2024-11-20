from pydantic import BaseModel
from datetime import datetime, date
from decimal import Decimal

class StgVacancies(BaseModel):
    id: int
    obj: str
    query_profession_eng_name: str
    query_dt: date
    update_ts: datetime

class StgExchangeRates(BaseModel):
    id: int
    obj: str
    query_dt: date
    update_ts: datetime

class DMMetrics(BaseModel):
    id: int
    city_name: str
    query_profession_eng_name: str
    dt: date
    cnt: int
    no_experience_cnt: int
    between_1_and_3_cnt: int
    between_3_and_6_cnt: int
    more_than_6_cnt: int
    no_experience_avg_salary: Decimal
    between_1_and_3_avg_salary: Decimal
    between_3_and_6_avg_salary: Decimal
    more_than_6_avg_salary: Decimal
    flexible_schedule_cnt: int
    remote_schedule_cnt: int
    full_day_schedule_cnt: int
    shift_schedule_cnt: int
    fly_in_fly_out_schedule_cnt: int

class DMSkills(BaseModel):
    id: int
    city_name: str
    query_profession_eng_name: str
    skill_name: str
    dt: date
    top: int
    cnt: int

class DCities(BaseModel):
    id: int
    name: str
    eng_name: str

class DProfessions(BaseModel):
    id: int
    name: str
    eng_name: str