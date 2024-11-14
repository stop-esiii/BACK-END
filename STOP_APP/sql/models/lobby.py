from STOP_APP.extensions import db


class Lobby(db.Model):

    __tablename__ = "Lobby"

    id = db.Column("id_lobby", db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.Integer, db.ForeignKey("User.id_user"), nullable=False)
    code_lobby = db.Column(db.String(4), unique=True, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    rounds = db.Column(db.Integer, nullable=False)
    max_members = db.Column(db.Integer, nullable=False)
    number_members = db.Column(db.Integer, nullable=False)
    themes = db.Column(db.Text)
    letters = db.Column(db.String(45), nullable=False)
    dt_insert = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    dt_update = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
