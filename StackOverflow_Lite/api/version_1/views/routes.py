import time
from collections import OrderedDict
from flask import Blueprint, jsonify, request
from ....models import models

mod = Blueprint('api', __name__)


@mod.route('/questions', methods=['GET', 'POST'])
def get_all_questions():
    if request.method == 'GET':
        if not models.questions:
            return jsonify({})
        else:
            select_query = request.args.get('select_query', None, str)
            if select_query:
                return_val = OrderedDict()
                for questionid in models.questions:
                    if select_query in models.questions[questionid].value:
                        return_val.update(
                                          {len(return_val) +
                                           1: models.questions[questionid]
                                           .unpack()})
                return jsonify(dict(return_val))
            return_val = OrderedDict()
            for questionid in models.questions:
                return_val[questionid] = models.questions[questionid].unpack()
            return jsonify(dict(return_val))
    else:
        sender = request.args.get('sender', default=None, type=str)
        quiz = request.args.get('quiz', default=None, type=str)
        if sender and quiz:
            my_quiz = models.Question(sender, quiz)
            models.questions.update({len(models.questions) + 1: my_quiz})
            return jsonify({'result': 'successful', 'time':
                            my_quiz.time_created})
        else:
            return jsonify({'error': 'no parameters received'})


@mod.route('/questions/<int:question_id>', methods=['GET'])
def get_specific_question(question_id):
    if len(models.questions) < question_id:
        return jsonify({'error': 'NOT FOUND', 'code': 404})
    elif question_id <= 0:
        return jsonify({'error': 'bad request'})
    else:
        return jsonify(models.questions[question_id].unpack())


@mod.route('/questions/<int:question_id>/answers', methods=['GET', 'POST'])
def get_post_answers(question_id):
    if len(models.questions) < question_id:
        return jsonify({'error': 'NOT FOUND', 'code': 404})
    elif question_id <= 0:
        return jsonify({'error': 'bad request'})
    else:
        if request.method == 'GET':
            val = models.questions[question_id].answers
            answers = OrderedDict()
            if not val:
                return jsonify({})
            else:
                for answerid in val:
                    answers[answerid] = models.answers[answerid].unpack()
                return jsonify(answers)
        else:
            sender = request.args.get('sender', None, str)
            answer = request.args.get('answer', None, str)
            if not (sender and answer):
                return jsonify({'error': 'missing parameters'})
            else:
                ans = models.Answer(sender, answer)
                models.questions[question_id].add_answer(ans)
                models.answers[len(models.answers) + 1] = ans
                return jsonify({'results':
                                'successful', 'time': ans.time_created})
