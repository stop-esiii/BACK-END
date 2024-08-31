from flask import Flask
from flask_jwt_extended import JWTManager
from STOP_APP import api
from STOP_APP import auth
from STOP_APP import manage
from STOP_APP.extensions import apispec
from STOP_APP.extensions import db
from STOP_APP.extensions import jwt
from STOP_APP.extensions import migrate
from STOP_APP.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from datetime import timedelta


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("STOP_APP")
    app.config.from_object("STOP_APP.config")

    if testing is True:
        app.config["TESTING"] = True

    # >>>>>>>>>Database Settings>>>>>>>>>
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    # <<<<<<<<<Database Settings<<<<<<<<<

    # >>>>>>>>>JWT Settings>>>>>>>>>
    app.config["JWT_SECRET_KEY"] = "HS256"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=10)
    # <<<<<<<<<JWT Settings<<<<<<<<<

    configure_extensions(app)
    configure_cli(app)
    configure_apispec(app)
    register_blueprints(app)

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    # >>>>>>>>>Ensures that the database and tables are created within the context of the app>>>>>>>>>
    db.init_app(app)
    with app.app_context():
        db.create_all()
    # <<<<<<<<<Ensures that the database and tables are created within the context of the app<<<<<<<<<
    jwt.init_app(app)
    migrate.init_app(app, db)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def configure_apispec(app):
    """Configure APISpec for swagger support"""
    apispec.init_app(app, security=[{"jwt": []}])
    apispec.spec.components.security_scheme(
        "jwt", {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    )
    apispec.spec.components.schema(
        "PaginatedResult",
        {
            "properties": {
                "total": {"type": "integer"},
                "pages": {"type": "integer"},
                "next": {"type": "string"},
                "prev": {"type": "string"},
            }
        },
    )


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(auth.views.blueprint)
    app.register_blueprint(api.views.blueprint)

application = create_app(testing=False)

if __name__ == "__main__":

    application.run(host="0.0.0.0", port=1245, debug=True, use_reloader=False, threaded=True) # use_reloader=False
