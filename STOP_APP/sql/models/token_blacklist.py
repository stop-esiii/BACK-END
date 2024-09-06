from STOP_APP.extensions import db


class TokenBlacklist(db.Model):

    __tablename__ = "TokenBlacklist"

    id = db.Column("id_token_blacklist", db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id_user"), nullable=False)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    token_type = db.Column(db.String(10), nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    dt_insert = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    dt_update = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
