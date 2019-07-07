from telebot import types
import string_worker
import config
from operator import itemgetter, attrgetter

time_to_typing = 2.5

def generate_list_enrolled_users(list_enrolled_user_data):
    f = open(config.enrolled_user_file,"w")
    f.write("count\tid\tfirst_name\tusername\n")
    for i,enrolled_user_data in enumerate(list_enrolled_user_data):
        f.write("{}\t{}\t{}\t{}\n".format(i + 1,enrolled_user_data.get_id(), enrolled_user_data.get_first_name(), enrolled_user_data.get_user_name()))
    f.close()

def generate_list_finished_users(list_finished_user_data):
    f = open(config.finished_user_file,"w")
    f.write("count\tid\tfirst_name\tusername\tpoints\tspended_time\n")
    for i,finished_user_data in enumerate(list_finished_user_data):
        f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(i + 1,finished_user_data.get_id(), finished_user_data.get_first_name(), finished_user_data.get_user_name(), 
                                            finished_user_data.get_points(), finished_user_data.get_spended_time()))
    f.close()

def generate_list_top_users(list_finished_user_data):
    list_finished_user_data.sort(key=lambda x: (-x.get_points(), x.get_spended_time()))
    f = open(config.top_user_file,"w")
    f.write("count\tid\tfirst_name\tusername\tpoints\tspended_time\n")
    for i,finished_user_data in enumerate(list_finished_user_data):
        f.write("{}\t{}\t{}\t{}\t{}\t{}\n".format(i + 1,list_finished_user_data[i].get_id(), list_finished_user_data[i].get_first_name(), list_finished_user_data[i].get_user_name(), 
                                            list_finished_user_data[i].get_points(), list_finished_user_data[i].get_spended_time()))
        if i >= 9:
        	break;

    f.close()

def generate_truth_lie_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

    markup.add(string_worker.get_right_answer_by_id(1))
    markup.add(string_worker.get_wrong_answer_by_id(1))

    return markup

