import hashlib
import random
from string import letters

class Crypto():

    '''
    
    A set of methods used in previous lessons 
    to hash and validate password
    imports hashlib, random and letters from string
    
    '''

    @classmethod
    def make_salt(cls, length = 5):

        '''
        Creates a random salt
        :param length: 
        :return: salt string 
        '''

        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_pw_hash(cls, name, pw, salt = None):

        '''
        Creates a password hashed based on the user's name, password and random salt
        :param name: username 
        :param pw: user's password
        :param salt: user's salt
        :return: Hashed password
        '''

        if not salt:
            salt = Crypto.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)

    @classmethod
    def valid_pw(cls, name, password, hashed, salt):

        '''
        Checks if a password is valid
        :param name: username
        :param password: user's password
        :param hashed: user's hashed password
        :param salt: user's salt
        :return: True if the hashed value is equal to a hash generated
        based on the name, password and salt of the user.
        '''

        return hashed == Crypto.make_pw_hash(name, password, salt)