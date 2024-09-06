from STOP_APP.sql.models import TokenBlacklist
from STOP_APP.extensions import db
from flask_jwt_extended import decode_token
from datetime import datetime
from sqlalchemy import and_


class AuthRepository():

    def add_token_to_database(self, user, access_token):
        # >>>>>>>>>Revoke all previous token if exists>>>>>>>>>
        tokens = TokenBlacklist.query.filter(and_(TokenBlacklist.id_user==user.id, TokenBlacklist.revoked==False)).all()
        for token in tokens:
            token.revoked = True
            token.dt_update = datetime.now()
        # <<<<<<<<<Revoke all previous token if exists<<<<<<<<<

        # >>>>>>>>>Update User>>>>>>>>>
        user.token = access_token
        user.dt_update = datetime.now()
        # <<<<<<<<<Update User<<<<<<<<<

        # >>>>>>>>>Append token>>>>>>>>>
        decoded_token = decode_token(access_token)
        jti = decoded_token["jti"]
        token_type = decoded_token["type"]
        expires = datetime.fromtimestamp(decoded_token["exp"])
        revoked = False
        model = TokenBlacklist(
            id_user=user.id,
            jti=jti,
            token_type=token_type,
            expires=expires,
            dt_insert=datetime.now(),
            dt_update=datetime.now(),
            revoked=revoked,
        )
        db.session.add(model)
        # <<<<<<<<<Append token<<<<<<<<<

        # Save changes
        db.session.commit()
        return True
