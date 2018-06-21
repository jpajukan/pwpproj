import connexion
import flask
import sys
sys.path.append('..')
sys.path.append('../..')

from pathlib import Path
from server import config
from server.db.models import db



def init_app(secret_key=config.secret, add_api=True):
    app = connexion.App(__name__, specification_dir="swagger/")
    if add_api:
        app.add_api(Path("api.yaml"))
    app.app.config["SECRET_KEY"] = secret_key
    return app


def init_db(app, db_uri=config.db_uri):
    db.app = app
    # Needed to get rid of warning on server start
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    db.init_app(app)
    db.create_all()
    return db


def static_host(path):
    return flask.send_from_directory("../client/", path)


if __name__ == '__main__':
    application = init_app()
    # Connexion adds another layer of abstraction to the Flask server object, so the DB needs to
    # be initialized with the app inside the app. Yo dawg...
    init_db(application.app)
    application.add_url_rule("/client/<path:path>", "client", static_host)
    application.run(host="0.0.0.0", debug=True)
