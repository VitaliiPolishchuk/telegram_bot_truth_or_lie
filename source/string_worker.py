from random import random
from config import shelve_name
import string_variables

def get_top_users():
    return string_variables.top_users

def get_list_enrolled_users():
    return string_variables.list_enrolled_users

def get_list_finished_users():
    return string_variables.list_finished_users

def get_only_one_time_game():
    return string_variables.only_one_time_game

def get_hello():
    return string_variables.hello

def get_invitation():
    return string_variables.invitation

def get_have_fun():
    return string_variables.have_fun

def get_want_to_play():
    return string_variables.want_to_play

def get_want_fun():
    return string_variables.want_fun

def get_result_message():
    return string_variables.result_message

def get_congratulation_0_6():
    return string_variables.congratulation_0_6

def get_congratulation_7():
    return string_variables.congratulation_7

def get_congratulation_more_7():
    return string_variables.congratulation_more_7

def get_profession_5():
    return string_variables.profession_5[random(0,1)]

def get_profession_6():
    return string_variables.profession_6[random(0,1)]

def get_profession_7():
    return string_variables.profession_7

def get_profession_more_7():
    return string_variables.profession_more_7

def get_right_answer_by_id(category_answer_id):
    return string_variables.truth_or_lie[category_answer_id - 1]

def get_wrong_answer_by_id(category_answer_id):
    if category_answer_id == 1:
        return string_variables.truth_or_lie[1]
    if category_answer_id == 2:
        return string_variables.truth_or_lie[0]



