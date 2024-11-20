from sqlalchemy import Column, ForeignKey, Integer, String, JSON, DateTime, Date, Numeric, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class StgVacancies(Base):
    __tablename__ = "stg_vacancies"

    id = Column(Integer, primary_key=True, nullable=False)
    obj = Column(JSON, nullable=False)
    query_profession_eng_name = Column(String(100), nullable=False)
    query_dt = Column(Date, nullable=False)
    update_ts = Column(DateTime, nullable=False)

class StgExchangeRates(Base):
    __tablename__ = "stg_exchange_rates"

    id = Column(Integer, primary_key=True, nullable=False)
    obj = Column(JSON, nullable=False)
    query_dt = Column(Date, nullable=False)
    update_ts = Column(DateTime, nullable=False)

class DCity(Base):
    __tablename__ = "d_city"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    eng_name = Column(String(100), nullable=False)

class DQueryProfession(Base):
    __tablename__ = "d_query_profession"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(100), nullable=False)
    eng_name = Column(String(100), nullable=False)

class DVacancies(Base):
    __tablename__ = "d_vacancies"

    id = Column(Integer, primary_key=True, nullable=False)
    vacancy_id = Column(Integer, nullable=False)
    city_id = Column(Integer, nullable=False)
    query_profession_id = Column(Integer, nullable=False)
    profession = Column(String(100))
    salary_currency = Column(String(10))
    salary_from = Column(Numeric(10, 2))
    salary_to = Column(Numeric(10, 2))
    experience = Column(String(20))
    schedule = Column(String(20))
    published_at = Column(DateTime)
    dt = Column(Date)
    uq_d_vacancies_vacancy_id_dt = UniqueConstraint('vacancy_id', 'dt')
    fk_d_vacancies_city = ForeignKey('city_id', 'd_city.id')
    fk_d_vacancies_query_profession = ForeignKey('query_profession_id', 'd_query_profession.id')

class DSkill(Base):
    __tablename__ = "d_skill"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(150), nullable=False)

class FctSkillVacancy(Base):
    __tablename__ = "fct_skill_vacancy"

    id = Column(Integer, primary_key=True, nullable=False)
    skill_id = Column(Integer, nullable=False)
    vacancy_id = Column(Integer, nullable=False)
    fk_fct_skill_vacancy_d_skill = ForeignKey('skill_id', 'd_skill.id')
    fk_fct_skill_vacancy_d_vacancies = ForeignKey('vacancy_id', 'd_vacancies.id')

class DExchangeRates(Base):
    __tablename__ = "d_exchange_rates"

    id = Column(Integer, primary_key=True)
    exchange_rates_id = Column(Integer, nullable=False)
    num_code = Column(String(5), nullable=False)
    char_code = Column(String(5), nullable=False)
    nominal = Column(Integer, nullable=False)
    name = Column(String(70), nullable=False)
    uq_d_exchange_rates_char_code = UniqueConstraint('char_code')

class FctExchangeRates(Base):
    __tablename__ = "fct_exchange_rates"

    id = Column(Integer, primary_key=True, nullable=False)
    id_exchange_rates = Column(Integer, nullable=False)
    value = Column(Numeric(10, 2), nullable=False)
    previous = Column(Numeric(10, 2), nullable=False)
    published_at = Column(DateTime, nullable=False)
    dt = Column(Date, nullable=False)

class DMMetrics(Base):
    __tablename__ = "dm_metrics"

    id = Column(Integer, primary_key=True, nullable=False)
    city_name = Column(String(100), nullable=False)
    query_profession_eng_name = Column(String(100), nullable=False)
    dt = Column(Date, nullable=False)
    cnt = Column(Integer, nullable=False)
    no_experience_cnt = Column(Integer, nullable=False)
    between_1_and_3_cnt = Column(Integer, nullable=False)
    between_3_and_6_cnt = Column(Integer, nullable=False)
    more_than_6_cnt = Column(Integer, nullable=False)
    no_experience_avg_salary = Column(Numeric(10, 2), nullable=False)
    between_1_and_3_avg_salary = Column(Numeric(10, 2), nullable=False)
    between_3_and_6_avg_salary = Column(Numeric(10, 2), nullable=False)
    more_than_6_avg_salary = Column(Numeric(10, 2), nullable=False)
    flexible_schedule_cnt = Column(Integer, nullable=False)
    remote_schedule_cnt = Column(Integer, nullable=False)
    full_day_schedule_cnt = Column(Integer, nullable=False)
    shift_schedule_cnt = Column(Integer, nullable=False)
    fly_in_fly_out_schedule_cnt = Column(Integer, nullable=False)
    dm_metrics_city_id_query_profession_id_dt = UniqueConstraint('city_name', 'query_profession_eng_name', 'dt')

class DMSkills(Base):
    __tablename__ = "dm_skills"

    id = Column(Integer, primary_key=True, nullable=False)
    city_name = Column(String(100), nullable=False)
    query_profession_eng_name = Column(String(100), nullable=False)
    skill_name = Column(String(150), nullable=False)
    dt = Column(Date, nullable=False)
    top = Column(Integer, nullable=False)
    cnt = Column(Integer, nullable=False)
    dm_skills_uq = UniqueConstraint('city_name', 'query_profession_eng_name', 'skill_name', 'dt')

