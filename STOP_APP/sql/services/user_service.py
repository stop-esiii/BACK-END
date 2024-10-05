from STOP_APP.sql.models import User
from STOP_APP.sql.repository import UserRepository
from sqlalchemy import or_


class UserService(UserRepository):

    def validate_username_email(self, payload):
        check_list = []
        if "username" in payload.keys():
            check_username = User.query.filter(or_(
                    User.username == payload["username"],
                    User.email == payload["username"]),
                    User.active == True
            ).first()
            if check_username is not None:
                check_list.append("Esse nome de usuário já existe.")
        if "email" in payload.keys():
            check_email = User.query.filter(or_(
                    User.email == payload["email"],
                    User.username == payload["email"]),
                    User.active == True
            ).first()
            if check_email is not None:
                check_list.append("Esse email já está em uso.")

        if len(check_list) != 0:
            return {"status": False, "msg": " / ".join(check_list)}
        return {"status": True}

    def add_user_service(self, payload):
        validate = self.validate_username_email(payload)
        if validate["status"]:
            result = self.add_user(payload)
            return {"status": True, "data": result}
        return validate

    def update_user_service(self, user, payload):
        validate = self.validate_username_email(payload)
        if validate["status"]:
            result = self.update_user(user, payload)
            return {"status": True, "data": result}
        return validate
