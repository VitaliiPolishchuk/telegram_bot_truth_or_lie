class EnrolledUserData:

    def __init__(self, row):
        self.id = row[0]
        self.first_name = row[1]
        self.user_name = row[2] 

    def get_id(self):
        return self.id

    def get_first_name(self):
        return self.first_name

    def get_user_name(self):
        return self.user_name