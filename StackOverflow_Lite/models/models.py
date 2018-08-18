import time
import collections


class User(object):

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.questions = collections.OrderedDict()
        self.answers = collections.OrderedDict()
        self.comments = collections.OrderedDict()
        self.time_created = time.asctime()
        return None

    def ask(self, question):
        self.questions.update({len(self.questions) + 1: question})
        return None

    def post_answer(self, answer):
        self.answers.update({len(self.answers) + 1: answer})
        return None

    def post_comment(self, comment):
        self.comments.update({len(self.comments) + 1: comment})
        return None

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


class Question(object):

    def __init__(self, sender, question):
        self.value = question
        self.answers = collections.OrderedDict()
        self.time_created = time.asctime()
        self.asker = sender
        return None

    def add_answer(self, answer):
        self.answers.update({len(self.answers) + 1: answer})
        return None

    def unpack(self):
        answers = collections.OrderedDict()
        for answer in self.answers:
            answers[answer] = self.answers[answer].unpack()
        return {'question': self.value, 'timePosted': self.time_created,
                'askedBy': self.asker, 'answers': dict(answers)}


class Answer(object):

    def __init__(self, sender, answer):
        self.value = answer
        self.comments = collections.OrderedDict()
        self.time_created = time.asctime()
        self.answerer = sender
        return None

    def add_comment(self, comment):
        self.comments.update({len(self.comments) + 1: comment})
        return None

    def unpack(self):
        comments = collections.OrderedDict()
        for comment in self.comments:
            comments[comment] = self.comments[comment].unpack()
        return {'answer': self.value, 'timePosted': self.time_created,
                'answeredBy': self.answerer, 'comments': dict(comments)}


class Comment(object):

    def __init__(self, sender, comment):
        self.value = comment
        self.time_created = time.asctime()
        self.commenter = sender
        return None

    def unpack(self):
        return {'comment': self.value, 'timePosted': self.time_created,
                'commentBy': self.commenter}


users = collections.OrderedDict()
questions = collections.OrderedDict()
answers = collections.OrderedDict()
comments = collections.OrderedDict()
