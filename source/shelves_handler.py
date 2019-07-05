from random import shuffle
from telebot import types
import shelve
from config import shelve_name


def save_user_data(chat_id, json):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить.
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = json

def get_user_data(chat_id):
    with shelve.open(shelve_name) as storage:
        try:
            json = storage[str(chat_id)]
            return json
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def delete_user_data(chat_id):
    """
    Заканчиваем игру текущего пользователя и удаляем правильный ответ из хранилища
    :param chat_id: id юзера
    """
    with shelve.open(shelve_name) as storage:
        del storage[str(chat_id)]