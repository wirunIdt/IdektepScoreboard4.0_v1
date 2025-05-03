class SubmissionDigitalTwin:
    def __init__(self, user, checkpoint1, checkpoint2, finish, score, time_taken, box_pass):
        self.user = user
        self.checkpoint1 = checkpoint1
        self.checkpoint2 = checkpoint2
        self.finish = finish
        self.score = score
        self.time_taken = time_taken
        self.box_pass = box_pass

    def to_dict(self):
        return {
            "user": self.user,
            "checkpoint1": self.checkpoint1,
            "checkpoint2": self.checkpoint2,
            "finish": self.finish,
            "score": self.score,
            "time_taken": self.time_taken,
            "box_pass": self.box_pass
        }

    @staticmethod
    def from_dict(data):
        return SubmissionDigitalTwin(
            data['user'],
            data['checkpoint1'],
            data['checkpoint2'],
            data['finish'],
            data['score'],
            data['time_taken'],
            data['box_pass']
        )
