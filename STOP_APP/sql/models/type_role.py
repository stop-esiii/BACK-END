from STOP_APP.extensions import db
from sqlalchemy import event, select


class TypeRole(db.Model):

    __tablename__ = "TypeRole"

    id = db.Column("id_type_role", db.Integer, primary_key=True)
    role = db.Column(db.String(45), unique=True, nullable=False)

@event.listens_for(TypeRole.__table__, 'after_create')
def create_roles(*args, **kwargs):
    # >>>>>>>>>Roles to add>>>>>>>>>
    roles = [
        "DEVELOPER", "ADMIN", "STANDARD",
        "PREMIUM"
    ]
    # <<<<<<<<<Roles to add<<<<<<<<<

    # Check if the roles already exist
    existing_roles = db.session.scalars(select(TypeRole.role)
                                        .filter(TypeRole.role.in_(roles))).all()

    # Filter out existing roles
    roles_to_add = [role for role in roles if role not in existing_roles]

    # >>>>>>>>>>>>Insert Roles>>>>>>>>>>>>
    if roles_to_add:
        db.session.bulk_save_objects([TypeRole(role=role) for role in roles_to_add])
        db.session.commit()
    # <<<<<<<<<Insert Roles<<<<<<<<<
