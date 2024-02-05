from aiogram import types

kb_start = [
    [types.KeyboardButton(text="Статистика")],
    [types.KeyboardButton(text="Тренажер")],
    [types.KeyboardButton(text="Теория слепой печати")],
    [types.KeyboardButton(text="Разработчики")]
]

kb_levels = [
    [types.KeyboardButton(text="Легкий")],
    [types.KeyboardButton(text="Средний")],
    [types.KeyboardButton(text="Сложный")],
    [types.KeyboardButton(text="Назад")]
]

kb_theory = [
    [types.KeyboardButton(text="Читать теорию")],
    [types.KeyboardButton(text="Назад")]
]

kb_back = [
    [types.KeyboardButton(text="Назад")]
]

kb_exit_in_menu = [
    [types.KeyboardButton(text="Выход в меню")]
]