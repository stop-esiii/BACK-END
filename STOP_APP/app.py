from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO
from STOP_APP.socket.resources import handle_create_lobby, handle_enter_lobby, handle_leave_lobby, \
                                      handle_disconnect_lobby, handle_trigger_stop, handle_validate_stop, \
                                      handle_return_stop, handle_receive_validate, handle_calculate_stop
from STOP_APP import api
from STOP_APP import manage
from STOP_APP.extensions import apispec
from STOP_APP.extensions import db
from STOP_APP.extensions import jwt
from STOP_APP.extensions import migrate
from STOP_APP.config import STOP_SQLALCHEMY_DATABASE_URI, STOP_SQLALCHEMY_TRACK_MODIFICATIONS, STOP_JWT_SECRET_KEY
from datetime import timedelta

def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("STOP_APP")
    app.config.from_object("STOP_APP.config")

    if testing is True:
        app.config["TESTING"] = True

    # >>>>>>>>>Database Settings>>>>>>>>>
    app.config["SQLALCHEMY_DATABASE_URI"] = STOP_SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = STOP_SQLALCHEMY_TRACK_MODIFICATIONS
    # <<<<<<<<<Database Settings<<<<<<<<<

    # >>>>>>>>>JWT Settings>>>>>>>>>
    app.config["JWT_SECRET_KEY"] = STOP_JWT_SECRET_KEY
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=10)
    # <<<<<<<<<JWT Settings<<<<<<<<<

    # >>>>>>>>>Settings>>>>>>>>>
    CORS(app)
    # <<<<<<<<<Settings<<<<<<<<<

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
    app.register_blueprint(api.views.blueprint)

application = create_app(testing=False)
socketio = SocketIO(application, cors_allowed_origins="*", async_mode="eventlet")

@socketio.on("create_lobby")
def create_lobby(data):
    handle_create_lobby(socketio, data)

@socketio.on("enter_lobby")
def enter_lobby(data):
    handle_enter_lobby(socketio, data)

@socketio.on("leave_lobby")
def leave_lobby(data):
    handle_leave_lobby(socketio, data)

@socketio.on("disconnect")
def disconnect():
    handle_disconnect_lobby(socketio)

@socketio.on("trigger_stop")
def stop(data):
    handle_trigger_stop(socketio, data)

@socketio.on("validate_stop")
def stop(data):
    handle_validate_stop(socketio, data)

@socketio.on("return_stop")
def stop(data):
    handle_return_stop(socketio, data)

@socketio.on("receive_validate")
def stop(data):
    handle_receive_validate(socketio, data)

@socketio.on("calculate_stop")
def stop(data):
    handle_calculate_stop(socketio, data)

if __name__ == "__main__":
    socketio.run(application, host="0.0.0.0", port=5000, debug=True)
