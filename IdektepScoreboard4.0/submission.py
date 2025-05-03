class Submission:
    def __init__(self, user, checkpoint1, checkpoint2, deduction, exp, finish, score, time_taken, age_group=None, comp_type=None):
        self.user = user
        self.checkpoint1 = checkpoint1
        self.checkpoint2 = checkpoint2
        self.score = score
        self.deduction = deduction
        self.exp = exp
        self.finish = finish
        self.time_taken = time_taken
        self.age_group = age_group
        self.comp_type = comp_type

    def to_dict(self):
        return {
            "user": self.user,
            "score": self.score,
            "time_taken": self.time_taken,
            "deduction": self.deduction,
            "checkpoint1" : self.checkpoint1,
            "checkpoint2" :self.checkpoint2,
            "exp" : self.exp,
            "finish" : self.finish,
            "age_group": self.age_group,
            "comp_type": self.comp_type
        }

    @staticmethod
    def from_dict(data):
        return Submission(
            data['user'], 
            data['checkpoint1'], data['checkpoint2'], 
            data['deduction'], data['exp'], data['finish'], 
            data['score'],data['time_taken'],
            data.get('age_group'), data.get('comp_type')
        )
