import time
from collections import OrderedDict
from flask import Blueprint, jsonify, request, make_response
from ....models import models

mod = Blueprint('api', __name__)


@mod.route('/questions', methods=['GET', 'POST'])
def get_all_questions():
    if request.method == 'GET':
        if not models.Question.questions:
            resp = make_response(jsonify(''))
            resp.status_code = 404
            resp.mimetype = 'application/json'
            return resp
        else:
            select_query = request.args.get('select_query', None, str)
            if select_query:
                return_val = OrderedDict()
                for questionid in models.Question.questions:
                    if select_query in models.Question.questions[questionid].value:
                        return_val.update(
                                          {len(return_val) +
                                           1: models.Question.questions[questionid]
                                           .unpack()})
                resp = make_response(jsonify(dict(return_val)))
                resp.status_code = 200
                resp.mimetype = 'application/json'
                return resp
            return_val = OrderedDict()
            for questionid in models.Question.questions:
                return_val[questionid] = models.Question.questions[questionid].unpack()
            resp = make_response(jsonify(dict(return_val)))
            resp.status_code = 200
            resp.mimetype = 'application/json'
            return resp
    else:
        sender = request.args.get('sender', default=None, type=str)
        quiz = request.args.get('quiz', default=None, type=str)
        if sender and quiz:
            my_quiz = models.Question(sender, quiz)
            resp = make_response(jsonify('question added'))
            resp.status_code = 200
            resp.mimetype = 'application/json'
            return resp
        else:
            resp = make_response(jsonify('no parameters'))
            resp.status_code = 400
            resp.mimetype = 'application/json'
            return resp


@mod.route('/questions/<int:question_id>', methods=['GET'])
def get_specific_question(question_id):
    if len(models.Question.questions) < question_id:
        resp = make_response(jsonify('NOT FOUND'))
        resp.status_code = 404
        resp.mimetype = 'application/json'
        return resp
    elif question_id <= 0:
        resp = make_response(jsonify('bad request'))
        resp.status_code = 400
        resp.mimetype = 'application/json'
        return resp
    else:
        resp = make_response(jsonify(models.Question.questions[question_id]
                                     .unpack()))
        resp.status_code = 200
        resp.mimetype = 'application/json'
        return resp


@mod.route('/questions/<int:question_id>/answers', methods=['GET', 'POST'])
def get_post_answers(question_id):
    if len(models.Question.questions) < question_id:
        resp = make_response(jsonify('NOT FOUND'))
        resp.status_code = 404
        resp.mimetype = 'application/json'
        return resp
    elif question_id <= 0:
        resp = make_response(jsonify('bad request'))
        resp.status_code = 400
        resp.mimetype = 'application/json'
        return resp
    else:
        select_query = request.args.get('select_query', None, str)
        if request.method == 'GET':
            val = models.Question.questions[question_id].answers
            answers = OrderedDict()
            if not val:
                resp = make_response(jsonify(''))
                resp.status_code = 404
                resp.mimetype = 'application/json'
                return resp
            else:
                if select_query:
                    for answerid in val:
                        if select_query in val[answerid].value:
                            answers[answerid] = val[answerid].unpack()
                    resp = make_response(jsonify(answers))
                    resp.status_code = 200 if answers else 404
                    resp.mimetype = 'application/json'
                    return resp
                for answerid in val:
                    answers[answerid] = val[answerid].unpack()
                resp = make_response(jsonify(answers))
                resp.status_code = 200
                resp.mimetype = 'application/json'
                return resp
        else:
            sender = request.args.get('sender', None, str)
            answer = request.args.get('answer', None, str)
            if not (sender and answer):
                resp = make_response(jsonify('missing parameters'))
                resp.status_code = 400
                resp.mimetype = 'application/json'
                return resp
            else:
                ans = models.Answer(sender, answer)
                models.Question.questions[question_id].add_answer(ans)
                resp = make_response(jsonify('answer posted'))
                resp.status_code = 201
                resp.mimetype = 'application/json'
                return resp


@mod.route('/questions/<int:question_id>/answers/<int:answer_id>/comments',
           methods=['GET', 'POST'])
def get_post_comments(question_id, answer_id):
    not_found = (question_id > len(models.Question.questions)) or (
                answer_id > len(models.Question.questions[question_id].answers))
    if not_found:
        resp = make_response(jsonify('NOT FOUND'))
        resp.status_code = 404
        resp.mimetype = 'application/json'
        return resp
    elif question_id <= 0 or answer_id <= 0:
        resp = make_response(jsonify('bad request'))
        resp.status_code = 400
        resp.mimetype = 'application/json'
        return resp
    else:
        if request.method == 'GET':
            comments = OrderedDict()
            comments_on_answer = (models.Question.questions[question_id]
                                  .answers[answer_id].comments)
            if not comments_on_answer:
                resp = make_response(jsonify(''))
                resp.status_code = 404
                resp.mimetype = 'application/json'
                return resp
            else:
                for commentid in comments_on_answer:
                    comments[commentid] = (comments_on_answer[commentid]
                                           .unpack())
                resp = make_response(jsonify(comments))
                resp.status_code = 200
                resp.mimetype = 'application/json'
                return resp
        else:
            sender = request.args.get('sender', None, str)
            comment = request.args.get('comment', None, str)
            if not (sender and comment):
                resp = make_response(jsonify('mising parameters'))
                resp.status_code = 400
                resp.mimetype = 'application/json'
                return resp
            else:
                comment = models.Comment(sender, comment)
                (models.Question.questions[question_id].answers[answer_id]
                 .add_comment(comment))
                resp = make_response(jsonify('answer posted'))
                resp.status_code = 201
                resp.mimetype = 'application/json'
                return resp
