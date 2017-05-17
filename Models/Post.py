from google.appengine.ext import db

class Post(db.Model):

    '''
    Post model
    '''

    user_id = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_at = db.DateTimeProperty(auto_now_add = True)
    up_votes = db.IntegerProperty(default = 0)
    down_votes = db.IntegerProperty(default = 0)
    last_modified = db.DateTimeProperty(auto_now = True)

    def add_up_vote(self):

        '''
        Adds up vote 
        '''

        self.up_votes += 1
        self.put()

    def add_down_vote(self):

        '''
        Adds down vote 
        '''

        self.down_votes  += 1
        self.put()

    @classmethod
    def get_post(cls, p_id):

        '''
        Retrieves a specific post
        :param p_id: post id
        :return: Post object
        '''

        key = db.Key.from_path('Post', int(p_id))
        return db.get(key)

    @classmethod
    def add(cls, user_id, author, title, content):

        '''
        Creates new post
        :param user_id: post's user id
        :param author: post's author
        :param title: post's title
        :param content: post's content
        :return: New Post object
        '''

        return Post(user_id=user_id, author=author, title=title, content=content)