

class User(object):

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.questions = {}
        self.answers = {}
        self.comments = {}
        return None

    def ask(self, question):
        self.questions.update({len(self.questions) + 1: question})
        return None

    def add_answer(self, answer):
        self.answers.update({len(self.answers) + 1: answer})
        return None

    def add_comment(self, comment):
        self.comments.update({len(self.comments) + 1: comment})
        return None


class Question(object):

    def __init__(self, question):
        self.value = question
        self.answers = {}
        return None

    def add_answer(self, answer):
        self.answers.update({len(self.answers) + 1: answer})
        return None


class Answer(object):

    def __init__(self, answer):
        self.value = answer
        self.comments = {}
        return None

    def add_comment(self, answer):
        self.comments.update({len(self.comments) + 1: comment})
        return None


class Comment(object):

    def __init__(self, comment):
        self.value = comment
        return None


users = {}
questions = {}
answers = {}
comments = {}
