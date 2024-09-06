from STOP_APP.sql.repository import Repository
from STOP_APP.sql.models import User, TokenBlacklist
from sqlalchemy import and_
import time


class Service:

    repository = Repository()

    # >>>>>>>>>SQL Functions>>>>>>>>>
    def get_by_id(self, id):
        return self.repository.get_by_id(id)

    def get_all(self, paginate: bool = False, page: int = None, per_page: int = None):
        return self.repository.get_all(paginate, page, per_page)

    def add(self, model):
        return self.repository.add(model)

    def delete(self, model):
        return self.repository.delete(model)

    def update(self, model, fields_update):
        return self.repository.update(model, fields_update)

    def commit_changes(self):
        return self.repository.commit_changes()
    # <<<<<<<<<SQL Functions<<<<<<<<<

    # >>>>>>>>>Function to get the execution time>>>>>>>>>
    def execution_time(self, begin = None):
        if begin == None:
            begin = time.time()
            return begin
        ExecutionTime = "{:.2f}".format(time.time() - begin)
        return ExecutionTime
    # <<<<<<<<<Function to get the execution time<<<<<<<<<

    # >>>>>>>>>Function to validate a request>>>>>>>>>
    def validate_request(serlf, claims):
        user = User.query.filter(and_(
            User.id==claims["id_user"],
            User.active==True)).first()
        token = TokenBlacklist.query.filter(and_(
            TokenBlacklist.id_user==claims["id_user"],
            TokenBlacklist.jti==claims["jti"],
            TokenBlacklist.revoked==False)).first()
        if user is None or token is None:
            return {"status": False, "msg": "Requisição inválida."}
        return {"status": True, "user": user, "token": token}
    # <<<<<<<<<Function to validate a request<<<<<<<<<

    # >>>>>>>>>Function to validate the permission of a user>>>>>>>>>
    def validate_permission(serlf, claims, permissions):
        user = User.query.filter(and_(
            User.id==claims["id_user"],
            User.id_type_role.in_(permissions),
            User.active==True)).first()
        if user is None:
            return {"status": False, "msg": "Permissão negada."}
        return {"status": True, "user": user}
    # <<<<<<<<<Function to validate the permission of a user<<<<<<<<<

    # >>>>>>>>>Function to verify if email exists>>>>>>>>>
    def validate_email(serlf, payload):
        user = User.query.filter(and_(
            User.email==payload["email"],
            User.active==True)).first()
        if user is None:
            return {"status": False, "msg": "email de usuário não encontrado."}
        return {"status": True, "user": user}
    # <<<<<<<<<Function to verify if email exists<<<<<<<<<
