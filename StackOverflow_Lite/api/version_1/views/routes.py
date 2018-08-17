import time
from flask import Blueprint, jsonify
from ....models import models

mod = Blueprint('api', __name__)


@mod.route('/questions', methods=['GET'])
def get_all_questions():
    pass
