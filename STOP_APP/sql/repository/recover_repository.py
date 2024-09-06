from STOP_APP.extensions import db
from STOP_APP.sql.models import VerificationCode
from datetime import datetime


class RecoverRepository():

    def disable_verification_codes(self, verification_codes):
        for vc in verification_codes:
            vc.active = False
            vc.dt_update = datetime.now()
        db.session.commit()
        return True

    def add_verification_code_to_database(self, user, verification_code):
        model = VerificationCode()
        model.id_user = user.id
        model.verification_code = verification_code
        model.dt_insert = datetime.now()
        model.dt_update = datetime.now()
        model.active = True
        db.session.add(model)
        # Save changes
        db.session.commit()
        return True

    def update_user_password(self, user, payload):
        user.password = payload["password"]
        user.dt_update = datetime.now()
        # Save changes
        db.session.commit()

    def disable_verification_code(self, verification_code):
        verification_code.active = 0
        verification_code.dt_update = datetime.now()
        # Save changes
        db.session.commit()
