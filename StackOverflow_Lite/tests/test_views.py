from flask import Flask, jsonify, make_response
from ..api.version_1.views import routes

app = Flask(__name__)
app.register_blueprint(routes.mod)

BASE_URL = 'http://127.0.0.1:5000/api/v1'


def test_get_all_questions():
    tester_app = app
    tester_ctx = tester_app.app_context()
    tester_ctx.push()
    tester_client = tester_app.test_client()
    response = tester_client.get(BASE_URL + '/questions')
    expected = make_response(jsonify({}))
    assert response == expected
    tester_ctx.pop()
