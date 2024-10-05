from STOP_APP.sql.models import User
from STOP_APP.extensions import db


class UserRepository():

    def add_user(self, data):
        model = User()
        model.id_type_role = data["id_type_role"]
        model.username = data["username"]
        model.email = data["email"]
        model.password = data["password"]
        model.image = None if "image" not in data.keys() else data["image"]
        db.session.add(model)
        db.session.commit()
        return model

    def update_user(self, user, data):
        user.id_type_role = data["id_type_role"] if "id_type_role" in data.keys() else user.id_type_role
        user.username = data["username"] if "username" in data.keys() else user.username
        user.email = data["email"] if "email" in data.keys() else user.email
        user.image = data["image"] if "image" in data.keys() else user.image
        user.themes = data["themes"] if "themes" in data.keys() else user.themes
        db.session.commit()
        return user
