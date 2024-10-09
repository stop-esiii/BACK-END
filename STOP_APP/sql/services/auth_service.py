from flask import current_app
from flask_jwt_extended import create_access_token
from STOP_APP.sql.services import Service
from STOP_APP.sql.repository import AuthRepository
from STOP_APP.sql.models import User
from STOP_APP.extensions import db
from sqlalchemy import or_
from datetime import timedelta, datetime


service = Service()


class AuthService(AuthRepository):

    def auth_user(self, payload):
        user = User.query.filter(or_(
            User.username==payload["login"],
            User.email==payload["login"]
        ), User.active==True).first()
        if user is None or not user.verify_password(payload["password"]):
            return {"status": False, "msg": "Credenciais inválidas."}
        else:
            additional_claims = {
                "id_user": user.id
            }
            access_token = create_access_token(identity=user.id, additional_claims=additional_claims, expires_delta=timedelta(hours=10))
            check = self.add_token_to_database(user, access_token)
            if check:
                return {"status": True, "id_user": user.id, "access_token": access_token}

    def revoke_user(self, validate):
        # >>>>>>>>>Logical deletion>>>>>>>>>
        validate["user"].token = None
        validate["user"].dt_update = datetime.now()
        validate["token"].revoked = True
        validate["token"].dt_update = datetime.now()
        # Save changes
        db.session.commit()
        # <<<<<<<<<Logical deletion<<<<<<<<<

        return {"status": True}
