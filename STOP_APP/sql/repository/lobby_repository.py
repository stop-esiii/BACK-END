from STOP_APP.sql.models import Lobby
from STOP_APP.extensions import db
from datetime import datetime
from sqlalchemy import and_
import random


class LobbyRepository():

    categories = [
        "Fruta", "Animal", "Cor",
        "CEP", "Filme", "Nome",
        "Profissão", "Objeto", "Flor",
        "Time", "Marca", "Personagem",
        "Comida", "Ator/Atriz", "Cantor/Banda",
        "Celebridade", "Adjetivo", "Programa de TV",
        "Doença", "Hobbie", "Super-herói",
        "Instrumento musical", "Carro", "Rio",
        "Idioma", "Esporte", "Parte do corpo",
        "Bebida", "Planta", "Tecnologia"
    ]

    def add_lobby(self, data, code_lobby):
        model = Lobby()
        model.id_user = data["id_user"]
        model.code_lobby = code_lobby
        model.time = data["time"]
        model.rounds = data["rounds"]
        model.max_members = data["max_members"]
        model.number_members = 1
        model.themes = str(random.sample(self.categories, 10)).replace("[", "").replace("]", "")
        model.dt_insert = datetime.now()
        model.dt_update = datetime.now()
        model.active = 1
        db.session.add(model)
        db.session.commit()
        return model
    
    def update_join_lobby(self, lobby):
        lobby.number_members = lobby.number_members + 1
        lobby.dt_update = datetime.now()
        db.session.commit()
        return lobby
    
    def update_leave_lobby(self, lobby):
        lobby.number_members = lobby.number_members - 1
        lobby.dt_update = datetime.now()
        db.session.commit()
        return lobby
    
    def update_disconnect_lobby(self, code_lobby):
        lobby = self.model.query.filter(and_(
            self.model.code_lobby==code_lobby,
            self.model.active==True)).first()
        if lobby is None:
            return None
        lobby.number_members = lobby.number_members - 1
        lobby.dt_update = datetime.now()
        db.session.commit()
        return lobby
