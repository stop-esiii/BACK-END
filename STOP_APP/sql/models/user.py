from STOP_APP.extensions import db, pwd_context
from STOP_APP.config import STOP_JWT_SECRET_KEY, STOP_JWT_ALGORITHM
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import event
from datetime import datetime, timedelta
import jwt


class User(db.Model):

    __tablename__ = "User"

    id = db.Column("id_user", db.Integer, primary_key=True)
    id_type_role = db.Column(db.Integer, db.ForeignKey("TypeRole.id_type_role"), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    image = db.Column(db.Text)
    dt_insert = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    dt_update = db.Column(db.DateTime(), default=db.func.current_timestamp(), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    token = db.Column(db.Text)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def verify_password(self, password):
        return pwd_context.verify(password, self._password)

    def generate_jwt(self):
        payload = {
            'id_user': self.id,
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token expiration time
        }
        self.token = jwt.encode(payload, STOP_JWT_SECRET_KEY, algorithm=STOP_JWT_ALGORITHM)
        db.session.commit()

    def invalidate_jwt(self):
        self.token = None
        db.session.commit()

@event.listens_for(User.__table__, 'after_create')
def create_admin_users(*args, **kwargs):
    users = []

    for i in range(1, 6):
        user = User(
            id_type_role=1,
            username=f"dev{i}",
            email=f"dev{i}@example.com",
            password="devdev",
            active=True
        )
        users.append(user)
    
    standard_user = User(
        id_type_role=3,
        username="standard",
        email="standard@example.com",
        password="devdev",
        active=True
    )
    users.append(standard_user)

    premium_user = User(
        id_type_role=4,
        username="premium",
        email="premium@example.com",
        password="devdev",
        active=True
    )
    users.append(premium_user)
    
    db.session.bulk_save_objects(users)
    db.session.commit()
