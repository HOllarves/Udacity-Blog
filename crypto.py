import hashlib
import random
from string import letters

class Crypto():

    '''
    
    A set of methods used in previous lessons 
    to hash and validate password
    
    '''

    @classmethod
    def make_salt(cls, length = 5):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_pw_hash(cls, name, pw, salt = None):
        if not salt:
            salt = Crypto.make_salt()
        h = hashlib.sha256(name + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)

    @classmethod
    def valid_pw(cls, name, password, hashed, salt):
        return hashed == Crypto.make_pw_hash(name, password, salt)