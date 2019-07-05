# -- coding utf-8 --
import sqlite3
from QuestionData import QuestionData
from EnrolledUserData import EnrolledUserData
from FinishedUserData import FinishedUserData

class SQLither:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all_enrolled_users(self):
        with self.connection:
            result = []
            for row in self.cursor.execute('SELECT * FROM enrolled_users').fetchall():
                result.append(EnrolledUserData(row))
            return result

    def select_all_finished_users(self):
        with self.connection:
            result = []
            for row in self.cursor.execute('SELECT * FROM finished_users').fetchall():
                result.append(FinishedUserData(row))
            return result

    def is_user_exist(self, user_id):
        with self.connection:
            return len(self.cursor.execute('SELECT * FROM enrolled_users WHERE Id = ?', (user_id,)).fetchall()) == 1

    def insert_enrolled_user(self, user_id, first_name, last_name):
        with self.connection:
            self.cursor.execute('INSERT INTO enrolled_users VALUES(?,?,?)', (user_id,first_name,last_name)).fetchall()

    def insert_finished_user(self, user_id, first_name, last_name, points, spended_time):
        with self.connection:
            self.cursor.execute('INSERT INTO finished_users VALUES(?,?,?,?,?)', (user_id,first_name,last_name, points, spended_time)).fetchall()

    def select_all(self):
        with self.connection:
            return self.cursor.execute('SELECT * FROM questions').fetchall()

    def select_all_answers(self):
        with self.connection:
            result = []
            for row in self.cursor.execute('SELECT * FROM category_answer').fetchall():
                result.append(row[1])
            return result

    def select_single_answer_by_question_id(self, question_id):
        with self.connection:
            return self.cursor.execute('SELECT category_answer.description FROM questions INNER JOIN category_answer on questions.true_category_answer = category_answer.Id WHERE questions.Id = ?', (question_id,)).fetchall()[0][0]


    def select_single_answer(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM category_answer WHERE Id = ?', (rownum,)).fetchall()[0][1]

    def select_all_not_answer(self, rownum):
        with self.connection:
            return self.cursor.execute('SELECT * FROM category_answer WHERE Id != ?', (rownum,)).fetchall()[0][1]

    def select_single_question(self, rownum):
        return QuestionData(self.cursor.execute('SELECT * FROM questions WHERE Id = ?', (rownum,)).fetchall()[0])

    def count_rows(self):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM questions').fetchall()
            return len(result)

    def select_description_of_proper_answer_question_id(self, question_id):
        with self.connection:
            
            return self.cursor.execute('SELECT answers.description FROM answers WHERE question_id = ? AND category_answer_id = (SELECT questions.true_category_answer FROM questions WHERE questions.Id = ?)',(question_id,question_id)).fetchall()[0][0]

    def select_description_of_wrong_answer_question_id(self, question_id):
        with self.connection:
            return self.cursor.execute('SELECT answers.description FROM answers WHERE question_id = ? AND category_answer_id != (SELECT questions.true_category_answer FROM questions WHERE questions.Id = ?)',(question_id,question_id)).fetchall()[0][0]

    # def insert_user(self, user_id, question_id):
    #     with self.connection:
    #         result = self.cursor.execute('INSERT INTO users VALUES (?,?)', (user_id, question_id))

    # def delete_user(self, user_id):
    #     with self.connection:
    #         result = self.cursor.execute('DELETE FROM users WHERE Id = ?', (user_id,))

    def close(self):
        self.cursor.close()
        self.connection.close()