import os
import json
from datetime import datetime

import logging
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)

API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
URL_REQ = f"http://{API_HOST}:{API_PORT}"

def __for_pie(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}% ({:d} )".format(pct, absolute)

def __delete_file_images_for_user(user_id: str) -> None:
    path_images = f'{os.getcwd()}/images'
    direct = os.listdir(path_images)
    for file in direct:
        if str(user_id) in file:
            path = os.path.join(path_images, file)
            os.remove(path)
            logger.info(f'File deleted - {path}')

def get_data_from_api(query: str, user_parameters_query: dict = {}) -> list:
    if query in ['metrics', 'skills']:
        parameters = {x:(user_parameters_query[x].strftime('%Y-%m-%d') \
                if type(user_parameters_query[x])==datetime else user_parameters_query[x]) \
                    for x in user_parameters_query }
        req_metric = requests.get(url=f"{URL_REQ}/{query}", params=parameters)
        value = json.loads(req_metric.content.decode(encoding='utf-8'))
        return value
    elif query in ['cities', 'professions']:
        req_data = requests.get(url=f"{URL_REQ}/{query}")
        value = json.loads(req_data.content.decode(encoding='utf-8'))
        return value
    else:
        raise ValueError("The query value must be metrics, skills, cities, professions.")

def get_path_image(user_id: str, command: str, value: dict)->str:
    try :
        __delete_file_images_for_user(user_id)
        df = pd.DataFrame(value)
        match command:
            case "cnt_vacancies":
                df_count = df[['dt', 'cnt', 'no_experience_cnt', 'between_1_and_3_cnt', 'between_3_and_6_cnt', 'more_than_6_cnt']]\
                    .sort_values('dt')\
                    .rename(columns={'dt': 'Даты',
                                    'cnt': 'Общее количество',
                                    'no_experience_cnt': 'Без опыта',
                                    'between_1_and_3_cnt': 'Опыт 1-3 года',
                                    'between_3_and_6_cnt': 'Опыт 3-6 лет',
                                    'more_than_6_cnt': 'Опыт более 6 лет'})
                logger.info(df_count)
                df_count.plot(x= 'Даты',
                        y=['Общее количество', 'Без опыта', 'Опыт 1-3 года', 'Опыт 3-6 лет', 'Опыт более 6 лет'],
                        ylabel='Количество',
                        grid=True,
                        title='Количество вакансий в зависимости от опыта',
                        figsize = (15.5, 6.5),
                        kind='line')
            case "avg_salary":
                df_salary = df[['no_experience_avg_salary', 'between_1_and_3_avg_salary', 'between_3_and_6_avg_salary', 'more_than_6_avg_salary']]
                df_salary['no_experience_avg_salary'] = df_salary['no_experience_avg_salary'].astype(float)
                df_salary['between_1_and_3_avg_salary'] = df_salary['between_1_and_3_avg_salary'].astype(float)
                df_salary['between_3_and_6_avg_salary'] = df_salary['between_3_and_6_avg_salary'].astype(float)
                df_salary['more_than_6_avg_salary'] = df_salary['more_than_6_avg_salary'].astype(float)
                df_salary = df_salary.rename(columns={'no_experience_avg_salary': 'Без опыта',
                                    'between_1_and_3_avg_salary': 'Опыт 1-3 года',
                                    'between_3_and_6_avg_salary': 'Опыт 3-6 лет',
                                    'more_than_6_avg_salary': 'Опыт более 6 лет'})\
                    .mean()
                logger.info(df_salary)
                df_salary.plot(y=['Без опыта', 'Опыт 1-3 года', 'Опыт 3-6 лет', 'Опыт более 6 лет'],
                        ylabel='Рубл.',
                        grid=True,
                        title='Средняя зарплата вакансий в зависимости от опыта',
                        figsize = (15.5, 6.5),
                        kind='bar',
                        rot=0)
            case "cnt_shedule":
                s_count_shedule = df[['flexible_schedule_cnt', 
                                      'remote_schedule_cnt', 
                                      'full_day_schedule_cnt', 
                                      'shift_schedule_cnt', 
                                      'fly_in_fly_out_schedule_cnt']]
                s_count_shedule = s_count_shedule.rename(columns={
                                    'flexible_schedule_cnt': 'Гибкий график',
                                    'remote_schedule_cnt': 'Удаленная работа',
                                    'full_day_schedule_cnt': 'Полный день',
                                    'shift_schedule_cnt': 'Сменный график',
                                    'fly_in_fly_out_schedule_cnt':'Вахтовый метод'
                                    })\
                                    .sum()  
                s_count_shedule = s_count_shedule.where(s_count_shedule>0).dropna()
                logger.info(s_count_shedule)
                s_count_shedule.plot(
                        title='Колличество вакансий в зависимости от режима работы (%)',
                        figsize = (15.5, 6.5),
                        legend=True,
                        autopct='%.1f',
                        kind='pie')
            case "skills":
                df_skills = df[['skill_name', 'cnt']]\
                        .groupby('skill_name')\
                        .sum('cnt')\
                        .reset_index()\
                        .rename(columns={'skill_name':'Навык', 'cnt':'Количество'})\
                        .sort_values(by='Количество', ascending=False)\
                        .head(30)
                
               

                df_skills.sort_values(by='Количество')\
                    .plot(
                        x='Навык',
                        xlabel='Количество',
                        ylabel='Навык',
                        grid=True,
                        title='Навыки требуемые в вакансиях',
                        color='green',
                        figsize = (18.5, 12),
                        kind='barh')
            case _:
                raise ValueError("Command not found.")
    finally:
        name_file = f'{os.getcwd()}/images/{command}_{user_id}_{datetime.now().strftime("%d_%m_%Y__%H_%M")}.png'
        plt.savefig(name_file)
        plt.close()
        return name_file
