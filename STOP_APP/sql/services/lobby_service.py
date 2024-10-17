from flask import current_app
from flask_socketio import leave_room
from STOP_APP.sql.services import Service
from STOP_APP.sql.repository import LobbyRepository
from STOP_APP.sql.models import Lobby, User
from STOP_APP.extensions import db
from sqlalchemy import or_, and_
from datetime import datetime
import random
import string


service = Service()


class LobbyService(LobbyRepository):

    model = Lobby()

    def generate_code(self, length=4):
        # Defining alphanumeric characters (letters and numbers)
        characters = string.ascii_letters + string.digits
        # Generating a random code with the desired length
        code = ''.join(random.choice(characters) for _ in range(length))
        return code

    def create_lobby(self, data):
        # Create "code_lobby"
        code_lobby = self.generate_code()
        # Save Lobby
        return self.add_lobby(data, code_lobby)
    
    def enter_lobby(self, data):
        # >>>>>>>>>Check if lobby exists or full>>>>>>>>>
        lobby = self.model.query.filter(and_(
            self.model.code_lobby==data["code_lobby"],
            self.model.active==True)).first()
        if lobby is None:
            return {"status": False, "msg": "Lobby not found."}
        if lobby.number_members == lobby.max_members:
            return {"status": False, "msg": "Lobby is full."}
        # <<<<<<<<<Check if lobby exists or full<<<<<<<<<

        # Update Lobby
        return self.update_join_lobby(lobby)
    
    def leave_lobby(self, data):
        # >>>>>>>>>Check if lobby exists or full>>>>>>>>>
        lobby = self.model.query.filter(and_(
            self.model.code_lobby==data["code_lobby"],
            self.model.active==True)).first()
        if lobby is None:
            return {"status": False, "msg": "Lobby not found."}
        # <<<<<<<<<Check if lobby exists or full<<<<<<<<<

        # Update Lobby
        return {
            "lobby": self.update_leave_lobby(lobby),
            "username": User().query.filter(
                User().id==data["id_user"]
            ).first().username
        }

    def disconnect_lobby(self, socketio, user_rooms):
        lobby_data = None
        for room in user_rooms:
            # Subtract one member of the room
            lobby = self.update_disconnect_lobby(room)
            if lobby is not None:
                lobby_data = lobby

            # Remove client of the room
            leave_room(socketio, room)

        # Check if any rooms have been found
        if lobby_data is None:
            return False
        return lobby_data.code_lobby
