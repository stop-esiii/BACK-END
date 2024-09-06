from flask import request
from flask_restful import Resource
from STOP_APP.api.schemas import RecoverSchemaPOST, RecoverSchemaPUT, UserSchemaGET
from STOP_APP.sql.services import Service, RecoverService


service = Service()
recover_service = RecoverService()


class RecoverResource(Resource):
    """Creation and get_all

    ---
    post:
      tags:
        - Recover
      summary: Generate a verification code
      description: Generate a verification code to change user password
      requestBody:
        content:
          application/json:
            schema:
              RecoverSchemaPOST
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
    put:
      tags:
        - Recover
      summary: Change password
      description: Change password by email and verification code
      requestBody:
        content:
          application/json:
            schema:
              RecoverSchemaPUT
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: boolean
                    example: true
                  user: UserSchemaGET
    """

    def post(self):
        try:
            # Load request
            payload = RecoverSchemaPOST().load(request.json)

            # >>>>>>>>>Validate request>>>>>>>>>
            validate = service.validate_email(payload)
            if not validate["status"]:
                return validate, 400
            # <<<<<<<<<Validate request<<<<<<<<<

            # Generate and store verification code
            verification_code = recover_service.verification_code_generate(validate["user"])

            # Send verification code by email
            return recover_service.verification_code_by_email(payload, verification_code["verification_code"]), 201
        except:
            return {"status": False, "msg": "Algo deu errado. Tente novamente."}, 400

    def put(self):
        # try:
            # Load request
            payload = RecoverSchemaPUT().load(request.json)

            # >>>>>>>>>Validate request>>>>>>>>>
            user = service.validate_email(payload)
            if not user["status"]:
                return user, 400
            verification_code = recover_service.validate_verification_code(user["user"], payload)
            if not verification_code["status"]:
                return verification_code, 400
            # <<<<<<<<<Validate request<<<<<<<<<

            # Change password
            return recover_service.change_password(user["user"], verification_code["verification_code"], payload), 200
        # except:
        #     return {"status": False, "msg": "Algo deu errado. Tente novamente."}, 400
