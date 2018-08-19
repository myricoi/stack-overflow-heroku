from flask import Flask

app = Flask(__name__)

from StackOverflow_Lite.api.version_1.views import routes
from StackOverflow_Lite.tests import test_views

app.register_blueprint(routes.mod, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)
