# -- coding utf-8 --
import sqlite3
import shelves_handler
import time

class UserData:

    question_limit = 0

    def __init__(self, chat_id):
        json = shelves_handler.get_user_data(chat_id)
        self.chat_id = chat_id
        if not json: 
            self.question_id = 0
            self.count_question = 0
            self.points = 0
            self.started_time = time.clock()
        else:
            self.question_id = json['question_id']
            self.count_question = json['count_question']
            self.points = json['points']
            self.started_time = json['started_time']

    def save(self):
        json = {}
        json['chat_id'] = self.chat_id
        json['question_id'] = self.question_id
        json['count_question'] = self.count_question
        json['points'] = self.points
        json['started_time'] = self.started_time
        print(json)
        shelves_handler.save_user_data(self.chat_id, json)

    def delete(self):
        shelves_handler.delete_user_data(self.chat_id)

    def get_question_id(self):
        return self.question_id

    def update_question(self, question_id):
        self.question_id = question_id
        self.count_question += 1

    def increase_points(self):
        self.points += 1

    def get_points(self):
        return self.points

    def is_solved_all_question(self):
        return self.points > self.question_limit

    def get_spended_time(self):
        return time.clock() - self.started_time;
