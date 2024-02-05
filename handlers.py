from aiogram import types, Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from utils import get_random_text, errors_text, add_user_in_table, get_statistics
from kb import kb_start, kb_levels, kb_theory, kb_exit_in_menu, kb_back
import time

router = Router()

last_handler = ""  # Последний использованный handler
choice_text = ""  # Выбранный текст для пользователя
start_time = 0


@router.message(
    Command("start"))
async def start_handler(msg: Message):
    global last_handler
    last_handler = "Старт"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_start,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    await msg.answer("Выберите нужный вариант:", reply_markup=keyboard)


@router.message(Text(text="Тренажер"))
async def message_handler_menu(msg: Message):
    global last_handler
    last_handler = "Тренажер"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_levels,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    await msg.answer("""Выберите уровень сложности:""", reply_markup=keyboard)


@router.message(Text(text=["Легкий", "Средний", "Сложный"]))
async def message_handler_levels(msg: Message):
    global last_handler, choice_text, start_time
    if last_handler == "Тренажер":
        text = ""
        if msg.text == "Легкий":
            text = get_random_text("1")
        elif msg.text == "Средний":
            text = get_random_text("2")
        elif msg.text == "Сложный":
            text = get_random_text("3")
        choice_text = text
        start_time = time.time()
        await msg.answer(f"Перепишите текст: {text}")
    last_handler = "Сложность"


@router.message(Text(text="Теория слепой печати"))
async def message_handler_theory(msg: Message):
    global last_handler
    last_handler = "Теория"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_theory,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    await msg.answer("""Нажмите Читать теорию""", reply_markup=keyboard)


@router.message(Text(text="Читать теорию"))
async def message_handler_statistic(msg: Message):
    global last_handler
    last_handler = "Читать теорию"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_back,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    await msg.answer("Ознакомьтесь с теорией слепой печати на компьютере."'\n\n'
                     "Исходное положение левой руки: мизинец на клавише «Ф», безымянный на «Ы», средний на «В», указательный на «А». "
                     "Исходное положение правой руки: мизинец на «Ж», безымянный на «Д», средний на «Л», указательный на «О». "
                     "Большие пальцы обеих рук располагаются на пробеле."
                     "«ФЫВА» и «ОЛДЖ» — это так называемые домашние клавиши. Чтобы быстро располагать руки в стартовую позицию, на клавишах «А» и «О» делают небольшие выступы. " '\n\n'
                     "Заниматься изучением десятипальцевого метода набора вслепую на компьютере желательно два-три раза в день. "
                     "Для начала попробуйте закрыть глаза и, расположив пальцы на домашней строке, напечатать свою фамилию. "
                     "Перемещайте только пальцы. Взгляд должен быть направлен не на клавиатуру, а на экран. "
                     "Продолжайте практиковаться в печатании слепым методом, пока не получится без ошибок. "
                     "Затем потренируйтесь в разделе 'Тренажер'", reply_markup=keyboard)


@router.message(Text(text="Статистика"))
async def message_handler_statistic(msg: Message):
    global last_handler
    last_handler = "Статистика"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_back,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    user = get_statistics(msg.chat.username)
    if user:
        await msg.answer(f"""Ваша статистика:
Текстов написано: {user[2]}
Рекорд по времени: {user[1]} символов/сек.""", reply_markup=keyboard)
    else:
        await msg.answer("Вы еще не напечатали ни одного текста", reply_markup=keyboard)


@router.message(Text(text="Разработчики"))
async def message_handler_about(msg: Message):
    global last_handler
    last_handler = "Разработчики"
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb_back,
        resize_keyboard=True,
        input_field_placeholder="Выберите команду"
    )
    await msg.answer("""С предложениями по улучшению бота обращаться к @diana_bakh или @gorokhov_se.""",
                     reply_markup=keyboard)


@router.message()
async def message_handler_text(msg: Message):
    global last_handler
    if last_handler == "Сложность":
        last_handler = "Текст"
        count_errors = errors_text(choice_text, msg.text)
        time_run = time.time() - start_time
        speed = round((len(choice_text) - count_errors) / time_run, 2)
        add_user_in_table(msg.chat.username, speed)
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb_exit_in_menu,
            resize_keyboard=True,
            input_field_placeholder="Выберите команду"
        )
        await msg.answer(f"Время: {round(time_run, 2)} секунд;\n"
                         f"Скорость: {speed} символов/сек.", reply_markup=keyboard)
    elif (msg.text == "Назад" or msg.text == "Выход в меню") and (last_handler == "Тренажер" or
                                                                  last_handler == "Читать теорию" or
                                                                  last_handler == "Разработчики" or
                                                                  last_handler == "Статистика",
                                                                  last_handler == "Текст"):
        last_handler = "Старт"
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb_start,
            resize_keyboard=True,
            input_field_placeholder="Выберите команду"
        )
        await msg.answer("Выберите нужный вариант:", reply_markup=keyboard)
