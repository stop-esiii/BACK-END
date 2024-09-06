from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from STOP_APP.extensions import apispec
from STOP_APP.api.resources import UserResource, UserList, AuthResource, \
                                   RecoverResource


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

# >>>>>>>>>USERS>>>>>>>>>
api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")
# <<<<<<<<<USERS<<<<<<<<<

# >>>>>>>>>AUTH>>>>>>>>>
api.add_resource(AuthResource, "/auth", endpoint="auth")
# <<<<<<<<<AUTH<<<<<<<<<

# >>>>>>>>>RECOVER>>>>>>>>>
api.add_resource(RecoverResource, "/recover", endpoint="recover")
# <<<<<<<<<RECOVER<<<<<<<<<

@blueprint.before_app_request
def register_views():

    # >>>>>>>>>USERS>>>>>>>>>
    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=UserList, app=current_app)
    # <<<<<<<<<USERS<<<<<<<<<

    # >>>>>>>>>AUTH>>>>>>>>>
    apispec.spec.path(view=AuthResource, app=current_app)
    # <<<<<<<<<AUTH<<<<<<<<<

    # >>>>>>>>>RECOVER>>>>>>>>>
    apispec.spec.path(view=RecoverResource, app=current_app)
    # <<<<<<<<<RECOVER<<<<<<<<<

@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
