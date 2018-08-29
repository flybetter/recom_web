from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return "hello world"

    from recom.main import map

    app.register_blueprint(map.bp)

    return app


if __name__ == '__main__':
    create_app()
