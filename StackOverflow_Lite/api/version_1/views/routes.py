from flask import Blueprint

mod = Blueprint('api', __name__)


@mod.route('/questions', methods=['GET'])
def get_all_questions():
    pass