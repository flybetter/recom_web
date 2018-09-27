from flask import Flask


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "hello world"

    from recom.main import map
    from recom.main import newhouse

    app.register_blueprint(map.bp)
    app.register_blueprint(newhouse.new_house)

    return app


if __name__ == '__main__':
    create_app()
