from flask import Flask
from StackOverflow_Lite.api.version_1.views import routes
app = Flask(__name__)

app.register_blueprint(routes.mod, url_prefix='/api/v1')

if __name__ == '__main__':
    app.run(debug=True)
