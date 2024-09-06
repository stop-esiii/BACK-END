from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from STOP_APP.api.schemas import AuthSchema
from STOP_APP.sql.services import Service, AuthService


service = Service()
auth_service = AuthService()


class AuthResource(Resource):
    """Authorize and Revoke Token

    ---
    post:
      tags:
        - Auth
      summary: Generate a access token
      description: Generate a access token
      requestBody:
        content:
          application/json:
            schema:
              AuthSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: boolean
                    example: true
                  access_token:
                    type: string
                    example: JWT string
    delete:
      tags:
        - Auth
      summary: Revoke a access token
      description: Revoke a access token
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  status:
                    type: boolean
                    example: true
    """

    def post(self):
        schema = AuthSchema()
        payload = schema.load(request.json)

        validate = auth_service.auth_user(payload)
        if validate["status"]:
            return validate, 201
        return validate, 400

    @jwt_required()
    def delete(self):
        # >>>>>>>>>Validate request>>>>>>>>>
        claims = get_jwt()
        validate = service.validate_request(claims)
        if not validate["status"]:
            return validate, 400
        # <<<<<<<<<Validate request<<<<<<<<<

        validate = auth_service.revoke_user(validate)
        if validate["status"]:
            return validate, 200
        return validate, 400
