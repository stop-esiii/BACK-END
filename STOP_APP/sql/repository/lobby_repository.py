from STOP_APP.sql.models import Lobby
from STOP_APP.extensions import db
from datetime import datetime
from sqlalchemy import and_


class LobbyRepository():

    def add_lobby(self, data, code_lobby):
        model = Lobby()
        model.id_user = data["id_user"]
        model.code_lobby = code_lobby
        model.time = data["time"]
        model.rounds = data["rounds"]
        model.max_members = data["max_members"]
        model.number_members = 1
        model.themes = data["themes"]
        model.dt_insert = datetime.now()
        model.dt_update = datetime.now()
        model.active = 1
        db.session.add(model)
        db.session.commit()
        return model
