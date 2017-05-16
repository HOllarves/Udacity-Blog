import hmac

SECRET = "65x1W&I98<6FS34^+1HwanWY4^^K#7"

class CookieHandler():

    '''
    Performs various operations with cookies
    imports hmac module
    '''

    @staticmethod
    def hash_str(s):

        '''
        Hashes input using HMAC algorithm
        :param s: String to be hashed
        :return: String value of the hash
        '''

        return hmac.new(SECRET, s).hexdigest()

    @classmethod
    def make_secure_val(cls, s):

        '''
        Creates cookie value
        :param s: String to be hashed
        :return: Cookie value with string|string format
        '''

        return "%s|%s" %(s, cls.hash_str(s))

    @classmethod
    def check_secure_val(cls, h):

        '''
        Checks if value of a cookie is valid
        :param h: cookie with name|value format
        :return: if valid, returns the cookie value.
        '''
        val = h.split("|")[0]
        if h == cls.make_secure_val(val):
            return val
