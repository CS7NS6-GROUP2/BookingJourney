import uuid
import datetime
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from dao import connection
from cassandra import ConsistencyLevel


class User(UserMixin):
    def __init__(self, id, car, name, password):
        self.id = id
        self.car = car
        self.name = name
        self.password = password

    def get_id(self):
        return self.id

    def validate_pwd(self, password):
        return self.password == password

    @staticmethod
    def get(id):
        user_lookup_stmt = connection.prepare("SELECT * FROM users WHERE id={}".format(id))
        user_lookup_stmt.consistency_level = ConsistencyLevel.QUORUM
        results = connection.execute(user_lookup_stmt)
        if results is None:
            return results
        ans = results.one()
        return User(str(ans[0]), ans[1], ans[2], ans[3])
