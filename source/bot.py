# -*- coding: utf-8 -*-
import config
import telebot
from SQLither import *
import string_worker, utils
from telebot import types
from UserData import UserData
from QuestionData import QuestionData
import time
from random import randint

bot = telebot.TeleBot(config.token)


def send_message(bot, chat_id, text,parse_mode=None,reply_markup=None):
    timeout = time.time() + 0
    while time.time() <= timeout:
        bot.send_chat_action(chat_id, 'typing')
    return bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup)


@bot.message_handler(commands=['start'])
def start(message):
	print(message.from_user.last_name)
	message = send_message(bot, message.chat.id, string_worker.get_hello())
	message = send_message(bot, message.chat.id, string_worker.get_invitation())
	# db_worker = SQLither(config.database_name)
	# for i in range(505, 1000):
		# db_worker.insert_enrolled_user(i, "first_name", "last_name")
		# db_worker.insert_finished_user(i, "first_name{}".format(i), "last_name".format(i), randint(0,12), randint(1,10000))
	# db_worker.close()
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	markup.add(string_worker.get_want_to_play())
	markup.add(string_worker.get_want_fun())
	if message.chat.id == config.admin_id:
		markup.add(string_worker.get_list_enrolled_users())
		markup.add(string_worker.get_list_finished_users())
		markup.add(string_worker.get_top_users())

	
		

	message = send_message(bot, message.chat.id, string_worker.get_have_fun(),reply_markup=markup)
	
	bot.register_next_step_handler(message, handle_main_menu_input)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_main_menu_input(message):
	if message.text == string_worker.get_want_to_play():
		db_worker = SQLither(config.database_name)
		if db_worker.is_user_exist(message.chat.id):
			message = send_message(bot, message.chat.id, string_worker.get_only_one_time_game())
			bot.register_next_step_handler(message, handle_main_menu_input)
			db_worker.close()
			return 
		db_worker.insert_enrolled_user(message.chat.id, message.from_user.first_name, message.from_user.last_name)
		db_worker.close()
		game(message)
	elif message.text == string_worker.get_want_fun():
		fun(message)

	elif message.text == string_worker.get_list_enrolled_users() and message.chat.id == config.admin_id:
		db_worker = SQLither(config.database_name)
		utils.generate_list_enrolled_users(db_worker.select_all_enrolled_users())
		db_worker.close()
		# bot.send_document(message.chat.id, open(config.enrolled_user_file, 'rb'))
	elif message.text == string_worker.get_list_finished_users() and message.chat.id == config.admin_id:
		db_worker = SQLither(config.database_name)
		utils.generate_list_finished_users(db_worker.select_all_finished_users())
		db_worker.close()
		# bot.send_document(message.chat.id, open(config.finished_user_file, 'rb'))
	elif message.text == string_worker.get_top_users() and message.chat.id == config.admin_id:
		db_worker = SQLither(config.database_name)
		utils.generate_list_top_users(db_worker.select_all_finished_users())
		db_worker.close()
		# bot.send_document(message.chat.id, open(config.top_user_file, 'rb'))


# def fun(message):


# @bot.message_handler(commands=['game'])
def game(message):
    # Подключаемся к БД
    db_worker = SQLither(config.database_name)
    
    # Получаем случайную строку из БД
    question_data = db_worker.select_single_question(1)

    user_data = UserData(message.chat.id)
    user_data.update_question(question_data.get_id())

    markup = utils.generate_truth_lie_markup()
    # Отправляем аудиофайл с вариантами ответа
    message = send_message(bot,message.chat.id, "*{}.* {}".format(user_data.get_question_id(),question_data.get_description()), parse_mode='markdown',reply_markup=markup)
    # Включаем "игровой режим"
    
    user_data.save()
    # Отсоединяемся от БД
    db_worker.close()
    bot.register_next_step_handler(message, check_answer)

def check_answer(message):
    # Если функция возвращает None -> Человек не в игре
    db_worker = SQLither(config.database_name)
    user_data = UserData(message.chat.id)
    answer = db_worker.select_single_answer_by_question_id(user_data.get_question_id())
    # Как Вы помните, answer может быть либо текст, либо None
    # Если None:
    # print(answer)
    print()
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        # Уберем клавиатуру с вариантами ответа.
        # Если ответ правильный/неправильный
        if message.text == answer:
        	#print(db_worker.select_description_of_proper_answer_question_id(user_data.get_question_id()))
            message_to_user = db_worker.select_description_of_proper_answer_question_id(user_data.get_question_id())
            user_data.increase_points()
        else:
            message_to_user = db_worker.select_description_of_wrong_answer_question_id(user_data.get_question_id())
        prev_message = message
        message = send_message(bot, message.chat.id, "_{}_".format(message_to_user), parse_mode="markdown")

    
    if(user_data.is_solved_all_question()):
    	result(message, user_data, prev_message)
    else:
    	game(message)


def result(message, user_data, prev_message):


	db_worker = SQLither(config.database_name)
	db_worker.insert_finished_user(prev_message.chat.id, prev_message.chat.first_name, prev_message.chat.last_name, user_data.get_points(), user_data.get_spended_time())
	db_worker.close()
	print(user_data.get_spended_time())
	points = user_data.get_points()

	keyboard_hider = types.ReplyKeyboardRemove()
	message_to_user_result = string_worker.get_result_message()
	message = send_message(bot,message.chat.id, message_to_user_result.format(points), reply_markup=keyboard_hider)

	if points == 5:
		message_profession_to_user = string_worker.get_profession_5()
	elif points == 6:
		message_profession_to_user = string_worker.get_profession_6()
	elif points == 7:
		message_profession_to_user = string_worker.get_profession_7()
	elif points > 7:
		message_profession_to_user = string_worker.get_profession_more_7()

	if points >= 5:
		message = send_message(bot,message.chat.id, message_profession_to_user)
	
	if points < 7:
		message_congratulation_to_user = string_worker.get_congratulation_0_6()
	elif points == 7:
		message_congratulation_to_user = string_worker.get_congratulation_7()
	else:
		message_congratulation_to_user = string_worker.get_congratulation_7()

	message = send_message(bot,message.chat.id, message_congratulation_to_user)

	user_data.delete()

	

if __name__ == '__main__':
    bot.polling(none_stop=True)