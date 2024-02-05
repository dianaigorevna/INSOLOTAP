import sqlite3
import random
from config import DB_NAME


def errors_text(text_good, text_user):
    """Подсчет количества ошибок между текстами"""
    errors = abs(len(text_good) - len(text_user))
    if len(text_good) > len(text_user):
        text_good = text_good[:len(text_user)]
    elif len(text_good) < len(text_user):
        text_user = text_user[:len(text_good)]
    for i in range(len(text_good)):
        if text_good[i] != text_user[i]:
            errors += 1
    return errors


def get_cursor_and_connection():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    return connection, cursor


def get_random_text(level: str):
    connection, cursor = get_cursor_and_connection()
    texts = cursor.execute(f"SELECT * FROM texts WHERE level={level}").fetchall()
    random_text = random.choice(texts)
    connection.close()
    return random_text[1]


def add_user_in_table(username, speed):
    connection, cursor = get_cursor_and_connection()
    user = cursor.execute(
        f"SELECT user_name, max_record, count_texts FROM users WHERE user_name='{username}'").fetchone()
    if not user:
        cursor.execute(f"INSERT INTO users (user_name, max_record, count_texts) VALUES ('{username}', {speed}, 1)")
        connection.commit()
    else:
        max_record = user[1]
        if speed < max_record and speed > 0:
            max_record = speed
        count_texts = user[2] + 1
        cursor.execute(
            f"UPDATE users SET max_record = {max_record}, count_texts = {count_texts} WHERE user_name = '{username}'")
        connection.commit()
    connection.close()


def get_statistics(username):
    connection, cursor = get_cursor_and_connection()
    user = cursor.execute(
        f"SELECT user_name, max_record, count_texts FROM users WHERE user_name='{username}'").fetchone()
    connection.close()
    return user
