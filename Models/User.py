from google.appengine.ext import db
from crypto import Crypto

class User(db.Model):
    username = db.StringProperty()
    password = db.StringProperty()
    password_salt = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)

    @classmethod
    def get(cls, user_id):
        key = db.Key.from_path('User', int(user_id))
        return db.get(key)

    @classmethod
    def get_by_name(cls, name):
        user = User.all().filter('username =', name).get()
        return user

    @classmethod
    def register(cls, username, password, email):
        user_salt = Crypto.make_salt(12)
        hashed_password = Crypto.make_pw_hash(username, password, user_salt)
        return User(username = username,
                    password = hashed_password,
                    password_salt = user_salt,
                    email = email)

    @classmethod
    def login(cls, username, password):
        user = cls.get_by_name(username)
        if user and Crypto.valid_pw(username, password, user.password, user.password_salt):
            return user