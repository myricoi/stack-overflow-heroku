from flask import Flask


app = Flask(__name__)
if __name__ == '__main__':
    from StackOverflow_Lite.api.version_1.views import routes
    app.register_blueprint(routes.mod, url_prefix='/api/v1')
    app.run()
