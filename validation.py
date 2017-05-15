import re

class Validation():


    ##### Validations method #######

    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

    @classmethod
    def valid_username(cls, username):
        return username and cls.USER_RE.match(username)

    PASS_RE = re.compile(r"^.{3,20}$")

    @classmethod
    def valid_password(cls, password):
        return password and cls.PASS_RE.match(password)

    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

    @classmethod
    def valid_email(cls, email):
        return not email or cls.EMAIL_RE.match(email)

    @classmethod
    def valid_title(cls, title):
        return len(title) > 5

    @classmethod
    def valid_content(self, content):
        return len(content) > 50