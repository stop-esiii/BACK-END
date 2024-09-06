from STOP_APP.extensions import db, pwd_context
from sqlalchemy.ext.hybrid import hybrid_property


class VerificationCode(db.Model):

    __tablename__ = "VerificationCode"

    id = db.Column("id_verification_code", db.Integer, primary_key=True)
    id_user = db.Column("id_user", db.Integer, db.ForeignKey("User.id_user"), nullable=False)
    _verification_code = db.Column("verification_code", db.Text)
    dt_insert = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    dt_update = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)

    @hybrid_property
    def verification_code(self):
        return self._verification_code

    @verification_code.setter
    def verification_code(self, value):
        self._verification_code = pwd_context.hash(value)

    def verify_verification_code(self, verification_code):
        return pwd_context.verify(verification_code, self._verification_code)
