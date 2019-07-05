class FinishedUserData:

    def __init__(self, row):
        self.id = row[0]
        self.first_name = row[1]
        self.last_name = row[2] 
        self.points = row[3] 
        self.spended_time = row[4]

    def get_id(self):
        return self.id

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_points(self):
        return self.points

    def get_spended_time(self):
        return self.spended_time    