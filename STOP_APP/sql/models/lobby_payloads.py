from STOP_APP.extensions import db


class LobbyPayloads(db.Model):

    __tablename__ = "LobbyPayloads"

    id = db.Column("id_payload", db.Integer, primary_key=True, autoincrement=True)
    id_lobby = db.Column(db.Integer, db.ForeignKey("Lobby.id_lobby"), nullable=False)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id_user"), nullable=False)
    letter = db.Column(db.String(1), nullable=False)
    user_payload = db.Column(db.Text, nullable=False)
    validation_payload = db.Column(db.Text, nullable=False)
    dt_insert = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    dt_update = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
