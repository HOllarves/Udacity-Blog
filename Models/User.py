from google.appengine.ext import db
from crypto import Crypto

class User(db.Model):

    '''
    User model
    imports Crypto
    '''

    username = db.StringProperty()
    password = db.StringProperty()
    password_salt = db.StringProperty()
    created = db.DateTimeProperty(auto_now_add = True)
    liked_posts = db.StringListProperty(default = None)


    def add_vote(self, post_id):
        self.liked_posts.append(post_id)
        self.put()

    @classmethod
    def get(cls, user_id):

        '''
        Retrieves a specific user
        :param user_id: user id
        :return: User object
        '''

        key = db.Key.from_path('User', int(user_id))
        return db.get(key)

    @classmethod
    def get_by_name(cls, name):

        '''
        Retrieves a specific user by name
        :param name: user's name
        :return: User object
        '''

        user = User.all().filter('username =', name).get()
        return user

    @classmethod
    def register(cls, username, password, email):

        '''
        Creates new user
        :param username: username 
        :param password: user's password
        :param email: user's email
        :return: new User object
        '''

        user_salt = Crypto.make_salt(12)
        hashed_password = Crypto.make_pw_hash(username, password, user_salt)
        return User(username = username,
                    password = hashed_password,
                    password_salt = user_salt,
                    liked_posts = [],
                    email = email)

    @classmethod
    def login(cls, username, password):

        '''
        Logs user
        :param username: username 
        :param password: user's password
        :return: If valid, User object
        '''

        user = cls.get_by_name(username)
        if user and Crypto.valid_pw(username, password, user.password, user.password_salt):
            return user