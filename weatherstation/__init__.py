import os
from flask import Flask


def create_app(test_config=None):
    """create and configure the app"""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        LATEST=os.path.join(app.instance_path, 'latest.json'),
        RAW=os.path.join(app.instance_path, 'raw.json')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import add, latest, raw, weather

    app.register_blueprint(add.bp)
    app.register_blueprint(latest.bp)
    app.register_blueprint(raw.bp)
    app.register_blueprint(weather.bp)

    return app
