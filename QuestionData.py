class QuestionData:

    def __init__(self, row):
        self.id = row[0]
        self.description = row[1]
        self.true_category_answer = row[2] 

    def get_id(self):
        return self.id

    def get_description(self):
        return self.description

    def get_true_category_answer(self):
        return self.true_category_answer