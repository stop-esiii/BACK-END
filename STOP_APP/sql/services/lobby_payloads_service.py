from flask import current_app
from STOP_APP.sql.services import Service
from STOP_APP.sql.repository import LobbyPayloadsRepository
from STOP_APP.sql.models import LobbyPayloads
from STOP_APP.extensions import db
from sqlalchemy import or_
from datetime import datetime


service = Service()


class LobbyPayloadsService(LobbyPayloadsRepository):

    model = LobbyPayloads()
