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
                    answers[answerid] = val[answerid].unpack()
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


@mod.route('/questions/<int:question_id>/answers/<int:answer_id>/comments',
           methods=['GET', 'POST'])
def get_post_comments(question_id, answer_id):
    not_found = (question_id > len(models.questions)) or (
                answer_id > len(models.answers))
    if not_found:
        return jsonify({'error': 'NOT FOUND'})
    elif question_id <= 0 or answer_id <= 0:
        return jsonify({'error': 'bad request'})
    else:
        if request.method == 'GET':
            comments = OrderedDict()
            comments_on_answer = (models.questions[question_id]
                                  .answers[answer_id].comments)
            if not comments_on_answer:
                return jsonify({})
            else:
                for commentid in comments_on_answer:
                    comments[commentid] = (comments_on_answer[commentid]
                                           .unpack())
                return jsonify(comments)
        else:
            sender = request.args.get('sender', None, str)
            comment = request.args.get('comment', None, str)
            if not (sender and comment):
                return jsonify({'error': 'no parameters send'})
            else:
                comment = models.Comment(sender, comment)
                models.comments[len(models.comments) + 1] = comment
                (models.questions[question_id].answers[answer_id]
                 .add_comment(comment))
                return jsonify({'results': 'success', 'time':
                                comment.time_created})
