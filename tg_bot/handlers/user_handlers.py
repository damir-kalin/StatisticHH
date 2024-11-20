import os
from datetime import datetime, timedelta
from copy import deepcopy
import logging

from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.callback_data import CallbackData
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback

from keyboards.inline_kb import create_inline_keyboard
from lexicon.lexicon import LEXICON, CITIES, PROFESSIONS
from database.database import user_dict_template, user_db
from services.services import get_data_from_api, get_path_image

router = Router()
dt_now = datetime.now()
dt_min_90 = dt_now - timedelta(days=90)
logger = logging.getLogger(__name__)

API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON[message.text])

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON[message.text])

@router.message(Command(commands='info'))
async def process_info_command(message: Message):
    await message.answer(text=LEXICON[message.text])

@router.message(Command(commands='run'))
async def process_run_command(message: Message):
    calendar = SimpleCalendar()
    calendar.set_dates_range(datetime(2024,6,1), datetime.now())
    user_db[message.from_user.id] = deepcopy(user_dict_template)
    await message.answer(text = LEXICON[message.text], reply_markup = await calendar.start_calendar(year=dt_min_90.year, month=dt_min_90.month))

@router.callback_query(F.data.in_(['cnt_vacancies', 'avg_salary', 'cnt_shedule', 'skills']))
async def process_start_dashbord_metrics(callback_query: CallbackQuery):
    logger.info(user_db[callback_query.from_user.id])
    if callback_query.data in ['cnt_vacancies', 'avg_salary', 'cnt_shedule']:
        result = get_data_from_api('metrics', user_db[callback_query.from_user.id])
    elif callback_query.data == 'skills':
        result = get_data_from_api('skills', user_db[callback_query.from_user.id])
    path_image = get_path_image(callback_query.from_user.id, callback_query.data, result)
    file = FSInputFile(path_image)
    await callback_query.message.delete()
    await callback_query.message.answer(text=LEXICON['parameters'] % (user_db[callback_query.from_user.id]['date_from'].strftime('%d.%m.%Y'),
                                        user_db[callback_query.from_user.id]['date_to'].strftime('%d.%m.%Y'),
                                        user_db[callback_query.from_user.id]['city'],
                                        user_db[callback_query.from_user.id]['profession']))
    await callback_query.message.answer_photo(photo=file)
    await callback_query.message.answer(text = LEXICON['quest'],
                                        reply_markup = create_inline_keyboard(1, ['cnt_vacancies', 'avg_salary', 'cnt_shedule', 'skills', 'reset']))

@router.callback_query(F.data == 'reset')
async def process_start_dashbord(callback_query: CallbackQuery):
    user_db[callback_query.message.from_user.id] = deepcopy(user_dict_template)
    await callback_query.message.edit_text(text = LEXICON['reset_success'])

@router.callback_query(F.data.in_(PROFESSIONS.keys()))
async def process_add_profession(callback_query: CallbackQuery):
    user_db[callback_query.from_user.id]['profession'] = PROFESSIONS[callback_query.data]
    await callback_query.message.edit_text(text = LEXICON['correct_profession'],
                                           reply_markup = create_inline_keyboard(1, CITIES.keys()))

@router.callback_query(F.data.in_(CITIES.keys()))
async def process_add_city(callback_query: CallbackQuery):
    user_db[callback_query.from_user.id]['city'] = callback_query.data
    await callback_query.message.edit_text(text=LEXICON['correct_city'],
                                           reply_markup=create_inline_keyboard(1, ['cnt_vacancies', 'avg_salary', 'cnt_shedule', 'skills', 'reset']))

@router.callback_query(SimpleCalendarCallback.filter())
async def process_simple_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    calendar = SimpleCalendar()
    calendar.set_dates_range(datetime(2024, 6, 1), datetime.now())
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        if user_db[callback_query.from_user.id]['date_from'] is None and type(date)==datetime:
            user_db[callback_query.from_user.id]['date_from'] = date
            await callback_query.message.edit_text(text=LEXICON['correct_start_date'],
                                                   reply_markup= await calendar.start_calendar(
                                                       year=datetime.now().year,
                                                       month=datetime.now().month))
        elif user_db[callback_query.from_user.id]['date_to'] is None and date > user_db[callback_query.from_user.id]['date_from'] and type(date)==datetime:
            user_db[callback_query.from_user.id]['date_to'] = date
            await callback_query.message.edit_text(text = LEXICON['correct_end_date'],
                                                   reply_markup = create_inline_keyboard(1, PROFESSIONS.keys()))
        else:
            await callback_query.message.edit_text(text = LEXICON['incorrect_date'])
