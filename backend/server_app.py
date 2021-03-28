from flask import Flask
from .blueprints.server import simon_server_blueprint
from os import path


def create_app(mode="development"):
    instance_path = path.join(
        path.abspath(path.dirname(__file__)), "../%s_instance" % mode
    )

    app = Flask("simon-backend",
                static_folder="static/",
                template_folder="template/",
                instance_path=instance_path,
                instance_relative_config=True)
    app.config.from_pyfile('config.cfg')
    app.register_blueprint(simon_server_blueprint)

    return app
