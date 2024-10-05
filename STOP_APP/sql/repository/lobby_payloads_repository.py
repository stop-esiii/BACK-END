from STOP_APP.sql.models import LobbyPayloads
from STOP_APP.extensions import db
from datetime import datetime
from sqlalchemy import and_


class LobbyPayloadsRepository():

    model = LobbyPayloads()
