from ..StackOverflow_Lite.models import models


def test_User_correctly_constructed():
    user = models.User('dickson', 'x@gmail.com', 'pass')
    a = [user.username, user.email, user.password,
         dict(user.questions), dict(user.answers),
         dict(user.comments)]
    assert a == ['dickson', 'x@gmail.com', 'pass',
                 {}, {}, {}]


def test_Question_correctly_constructed():
    quiz = models.Question('dickson', 'where is Andela?')
    a = [quiz.asker, quiz.value, dict(quiz.answers)]
    assert a == ['dickson', 'where is Andela?', {}]


def test_Answer_correctly_constructed():
    ans = models.Answer('dickson', 'near TRM')
    a = [ans.answerer, ans.value, dict(ans.comments)]
    assert a == ['dickson', 'near TRM', {}]


def test_Comment_correctly_constructed():
    com = models.Comment('dickson', 'thanks')
    a = [com.commenter, com.value]
    assert a == ['dickson', 'thanks']


def test_classes_correctly_build_up_1():
    user = models.User('dickson', 'x@gmail.com', 'pass')
    quiz = models.Question('dickson', 'who am I')
    ans = models.Answer('manu', 'who you are')
    com = models.Comment('dickson', '@manu yeah')
    user.ask(quiz)
    quiz.add_answer(ans)
    ans.add_comment(com)
    assert isinstance(user.questions[1].answers[1]
                      .comments[1], models.Comment)
    assert isinstance(user.questions[1].answers[1],
                      models.Answer)
    assert isinstance(user.questions[1],
                      models.Question)


def test_classes_correctly_build_up_2():
    dickson = models.User('dickson', 'x@gmail.com',
                          'pass')
    manu = models.User('manu', 'y@gmail.com', 'pass2')
    quiz = models.Question('dickson', 'who am I')
    ans = models.Answer('manu', 'who you are')
    com = models.Comment('dickson', 'yeah')
    dickson.ask(quiz)
    manu.post_answer(ans)
    dickson.post_comment(com)
    quiz.add_answer(ans)
    ans.add_comment(com)
    json1 = {'comment': 'yeah', 'timePosted':
             ans.time_created, 'commentBy': 'dickson'}
    assert com.unpack() == json1


def test_classes_correctly_build_up_3():
    dickson = models.User('dickson', 'x@gmail.com',
                          'pass')
    manu = models.User('manu', 'y@gmail.com', 'pass2')
    quiz = models.Question('dickson', 'who am I')
    ans = models.Answer('manu', 'who you are')
    com = models.Comment('dickson', 'yeah')
    dickson.ask(quiz)
    manu.post_answer(ans)
    dickson.post_comment(com)
    quiz.add_answer(ans)
    ans.add_comment(com)
    json2 = {'answer': 'who you are', 'timePosted':
             ans.time_created, 'answeredBy': 'manu',
             'comments': {1: {'comment': 'yeah', 'timePosted':
                              ans.time_created, 'commentBy':
                              'dickson'}}}
    assert json2 == ans.unpack()


def test_classes_correctly_build_up_4():
    dickson = models.User('dickson', 'x@gmail.com', 'pass')
    manu = models.User('manu', 'y@gmail.com', 'pass2')
    quiz = models.Question('dickson', 'who am I')
    ans = models.Answer('manu', 'who you are')
    com = models.Comment('dickson', 'yeah')
    dickson.ask(quiz)
    manu.post_answer(ans)
    dickson.post_comment(com)
    quiz.add_answer(ans)
    ans.add_comment(com)
    json3 = {'question': 'who am I', 'timePosted':
             quiz.time_created, 'askedBy': 'dickson',
             'answers': {1: {'answer': 'who you are',
                             'timePosted': ans.time_created,
                             'answeredBy': 'manu', 'comments':
                             {1: {'comment': 'yeah', 'timePosted':
                                  ans.time_created, 'commentBy':
                                  'dickson'}}}}}
    assert quiz.unpack() == json3


def test_classes_correctly_build_up_5():
    dickson = models.User('dickson', 'x@gmail.com', 'pass')
    manu = models.User('manu', 'y@gmail.com', 'pass2')
    quiz = models.Question('dickson', 'who am I')
    ans = models.Answer('manu', 'who you are')
    com = models.Comment('dickson', 'yeah')
    dickson.ask(quiz)
    manu.post_answer(ans)
    dickson.post_comment(com)
    quiz.add_answer(ans)
    ans.add_comment(com)
    json = {'user': 'dickson', 'email': 'x@gmail.com',
            'signedUp': dickson.time_created, 'questionsPosted':
            {1: {'question': 'who am I', 'timePosted': quiz.time_created,
                 'askedBy': 'dickson', 'answers':
                 {1: {'answer': 'who you are', 'timePosted': ans.time_created,
                      'answeredBy': 'manu', 'comments':
                      {1: {'comment': 'yeah', 'timePosted': ans.time_created,
                           'commentBy': 'dickson'}}}}}},
            'answersPosted': {},
            'commentsMade': {1: {'comment': 'yeah', 'timePosted':
                                 ans.time_created,
                                 'commentBy': 'dickson'}}}
    assert dickson.unpack() == json
