from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt
from STOP_APP.api.schemas import UserSchemaPOST, UserSchemaGET, UserSchemaPUT
from STOP_APP.sql.models import User
from STOP_APP.extensions import db
from STOP_APP.commons.pagination import paginate
from STOP_APP.sql.services import Service, UserService
from datetime import datetime


service = Service()
service_user = UserService()


class UserResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - Users
      summary: Get a user
      description: Get a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  user: UserSchemaGET
        404:
          description: user does not exists
    put:
      tags:
        - Users
      summary: Update a user
      description: Update a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              UserSchemaPUT
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Usuário atualizado.
                  user: UserSchemaGET
        404:
          description: user does not exists
    delete:
      tags:
        - Users
      summary: Delete a user
      description: Delete a single user by ID
      parameters:
        - in: path
          name: user_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Usuário deletado.
        404:
          description: user does not exists
    """

    method_decorators = [jwt_required()]

    def get(self, user_id):
        # >>>>>>>>>Validate request>>>>>>>>>
        claims = get_jwt()
        validate = service.validate_request(claims)
        if not validate["status"]:
            return validate, 400
        validate = service.validate_permission(claims, [1, 2, 3, 4])
        if not validate["status"]:
            return validate, 400
        # if validate["user"].id != user_id:
        #     return {"status": False, "msg": "Operação inválida."}, 400
        # <<<<<<<<<Validate request<<<<<<<<<

        schema = UserSchemaGET()
        user = User.query.filter_by(id=user_id, active=True).first_or_404()
        return {"user": schema.dump(user)}, 200

    def put(self, user_id):
        # >>>>>>>>>Validate request>>>>>>>>>
        claims = get_jwt()
        validate = service.validate_request(claims)
        if not validate["status"]:
            return validate, 400
        validate = service.validate_permission(claims, [1, 2, 3, 4])
        if not validate["status"]:
            return validate, 400
        if validate["user"].id != user_id:
            return {"status": False, "msg": "Operação inválida."}, 400
        # <<<<<<<<<Validate request<<<<<<<<<

        user = User.query.filter_by(id=user_id, active=True).first_or_404()

        # Load request
        payload = UserSchemaPUT().load(request.json)

        # Update user in DataBase
        user = service_user.update_user_service(user, payload)
        if not user["status"]:
            return user, 400

        return {"msg": "Usuário atualizado.", "user": UserSchemaGET().dump(user["data"])}, 200

    def delete(self, user_id):
        # >>>>>>>>>Validate request>>>>>>>>>
        claims = get_jwt()
        validate = service.validate_request(claims)
        if not validate["status"]:
            return validate, 400
        validate = service.validate_permission(claims, [1, 2])
        if not validate["status"]:
            return validate, 400
        # <<<<<<<<<Validate request<<<<<<<<<

        User.query.filter_by(id=user_id, active=True).first_or_404()
        # >>>>>>>>>Logical exclusion>>>>>>>>>
        User.query.filter(User.id==user_id).update({
            "active": 0,
            "dt_update": datetime.now()
        })
        db.session.commit()
        # <<<<<<<<<Logical exclusion<<<<<<<<<

        return {"msg": "Usuário deletado."}, 200

class UserList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - Users
      summary: Get a list of users
      description: Get a list of paginated users
      responses:
        200:
          content:
            application/json:
              schema:
                properties:
                  results:
                    type: array
                    items: UserSchemaGET
    post:
      tags:
        - Users
      summary: Create a user
      description: Create a new user
      requestBody:
        content:
          application/json:
            schema:
              UserSchemaPOST
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: Usuário criado.
                  user: UserSchemaPOST
    """

    @jwt_required()
    def get(self):
        # >>>>>>>>>Validate request>>>>>>>>>
        claims = get_jwt()
        validate = service.validate_request(claims)
        if not validate["status"]:
            return validate, 400
        validate = service.validate_permission(claims, [1, 2])
        if not validate["status"]:
            return validate, 400
        # <<<<<<<<<Validate request<<<<<<<<<

        schema = UserSchemaGET(many=True)
        query = User.query.filter_by(active=True)
        return paginate(query, schema), 200

    def post(self):
        # Load request
        payload = UserSchemaPOST().load(request.json)

        # Add user in DataBase
        user = service_user.add_user_service(payload)
        if not user["status"]:
            return user, 400

        return {"msg": "Usuário criado.", "user": UserSchemaGET().dump(user["data"])}, 201
