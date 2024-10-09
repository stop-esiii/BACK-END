from STOP_APP.sql.models import Lobby
from STOP_APP.extensions import db
from datetime import datetime
from sqlalchemy import and_
import random


class LobbyRepository():

    categories = [
        "Frutas", "Animais", "Cores",
        "CEP (Cidades, Estados e Países)", "Filmes", "Nomes próprios",
        "Profissões", "Objetos", "Flores",
        "Times de futebol", "Marcas", "Personagens fictícios",
        "Comidas", "Atores/Atrizes", "Cantores/Bandas",
        "Celebridades", "Adjetivos", "Programas de TV",
        "Doenças", "Hobbies", "Super-heróis",
        "Instrumentos musicais", "Carros", "Rios",
        "Línguas", "Esportes", "Partes do corpo",
        "Bebidas", "Plantas", "Tecnologia"
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
