import time
import collections


class User():
    
    users = collections.OrderedDict()

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.questions = collections.OrderedDict()
        self.answers = collections.OrderedDict()
        self.comments = collections.OrderedDict()
        self.time_created = time.asctime()
        User.users.update({len(User.users) + 1: self})

    def ask(self, question):
        self.questions.update({len(self.questions) + 1: question})

    def post_answer(self, answer):
        self.answers.update({len(self.answers) + 1: answer})

    def post_comment(self, comment):
        self.comments.update({len(self.comments) + 1: comment})

    def unpack(self):
        questions = collections.OrderedDict()
        answers = collections.OrderedDict()
        comments = collections.OrderedDict()
        for question in self.questions:
            questions[question] = self.questions[question].unpack()
        for answer in self.answers:
            answers[answer] = self.answers[answer].unpack()
        for comment in self.comments:
            comments[comment] = self.comments[comment].unpack()
        od = collections.OrderedDict([('user', self.username),
                                      ('email', self.email),
                                      ('signedUp', self.time_created),
                                      ('questionsPosted', dict(questions)),
                                      ('answersPosted', dict(answers)),
                                      ('commentsMade', dict(comments))])
        return dict(od)


class Question():

    questions = collections.OrderedDict()

    def __init__(self, sender, question):
        self.value = question
        self.answers = collections.OrderedDict()
        self.time_created = time.asctime()
        self.asker = sender
        Question.questions.update({len(Question.questions) + 1: self})

    def add_answer(self, answer):
        self.answers.update({len(self.answers) + 1: answer})

    def unpack(self):
        answers = collections.OrderedDict()
        for answer in self.answers:
            answers[answer] = self.answers[answer].unpack()
        return {'question': self.value, 'timePosted': self.time_created,
                'askedBy': self.asker, 'answers': dict(answers)}


class Answer():

    answers = collections.OrderedDict()

    def __init__(self, sender, answer):
        self.value = answer
        self.comments = collections.OrderedDict()
        self.time_created = time.asctime()
        self.answerer = sender
        Answer.answers.update({len(Answer.answers) + 1: self})

    def add_comment(self, comment):
        self.comments.update({len(self.comments) + 1: comment})

    def unpack(self):
        comments = collections.OrderedDict()
        for comment in self.comments:
            comments[comment] = self.comments[comment].unpack()
        return {'answer': self.value, 'timePosted': self.time_created,
                'answeredBy': self.answerer, 'comments': dict(comments)}


class Comment():

    comments = collections.OrderedDict()

    def __init__(self, sender, comment):
        self.value = comment
        self.time_created = time.asctime()
        self.commenter = sender
        Comment.comments.update({len(Comment.comments) + 1: self})

    def unpack(self):
        return {'comment': self.value, 'timePosted': self.time_created,
                'commentBy': self.commenter}

