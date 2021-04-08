import uuid
import datetime

from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

USERS = [
    {
        "user_id": 1,
        "user_name": 'nnjj',
        "password": generate_password_hash('123')
    },
    {
        "user_id": 2,
        "user_name": 'xxrr',
        "password": generate_password_hash('123')
    }
]


class User(UserMixin):
    def __init__(self, user):
        self.username = user.get("user_name")
        self.password_hash = user.get("password")
        self.id = user.get("user_id")

    # class User(Model):
    # user_id = columns.UUID(primary_key=True, default=uuid.uuid4)
    # user_name = columns.Text(required=True)
    # password = columns.Text(required=True)
    # time = columns.DateTime(default=datetime.datetime.now)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.id

    @staticmethod
    def get_user(username):
        for user in USERS:
            if user.get("user_name") == username:
                return User(user)
        return None

    @staticmethod
    def get(user_id):
        if not user_id:
            return None
        for user in USERS:
            if user.get('id') == user_id:
                return User(user)
        return None
