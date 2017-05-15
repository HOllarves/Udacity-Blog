import hmac

SECRET = "65x1W&I98<6FS34^+1HwanWY4^^K#7"

class CookieHandler():

    @staticmethod
    def hash_str(s):
        #Hashes input using HMAC algorithm
        return hmac.new(SECRET, s).hexdigest()

    @classmethod
    def make_secure_val(cls, s):
        #Creates cookie value
        return "%s|%s" %(s, cls.hash_str(s))

    @classmethod
    def check_secure_val(cls, h):
        #Checks if value is valid
        val = h.split("|")[0]
        if h == cls.make_secure_val(val):
            return val
