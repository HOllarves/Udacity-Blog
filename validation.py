import re

class Validation():

    '''
    Validation methods for strings
    imports re
    '''

    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")  # User validation regex
    PASS_RE = re.compile(r"^.{3,20}$")  # Password validation regex
    EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')  # Email validation regex

    @classmethod
    def valid_username(cls, username):

        '''
        Checks if a username is valid
        :param username: username to be validated
        :return: username if valid
        '''

        return username and cls.USER_RE.match(username)

    @classmethod
    def valid_password(cls, password):

        '''
        Checks if a password is valid
        :param password: password to be validated
        :return: password if valid
        '''

        return password and cls.PASS_RE.match(password)

    @classmethod
    def valid_email(cls, email):

        '''
        Checks if an email is valid
        :param email: email to be validated
        :return: email if valid
        '''

        return not email or cls.EMAIL_RE.match(email)

    @classmethod
    def valid_title(cls, title):

        '''
        Checks if a title for a post is valid
        :param title: title to be validated
        :return: Title if it's longer than 5 words
        '''

        return len(title) > 5

    @classmethod
    def valid_content(self, content):

        '''
        Checks if content for a post is valid
        :param content: content to be validated 
        :return: Content if it's longer than 50 words
        '''

        return len(content) > 50