from google.appengine.ext import db

class Comment(db.Model):

    '''
    Comment model.
    '''

    username = db.StringProperty(required = True)
    user_id = db.StringProperty(required = True)
    post_id = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_at = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def get_comment(cls, c_id):

        '''
        Retrieves a specific comment 
        :param c_id: comment id
        :return: Comment object
        '''

        key = db.Key.from_path('Comment', int(c_id))
        return db.get(key)

    @classmethod
    def add(cls, username, u_id, p_id, content):

        '''
        Creates new comment
        :param username: comment's username
        :param u_id: comment's user id
        :param p_id: comment's post id
        :param content: comment's content
        :return: new Comment object
        '''

        return Comment(username= username, user_id=u_id, post_id=p_id, content=content)

    @classmethod
    def by_post_id(cls, post_id):

        '''
        Retrieves all comments associated with a post
        :param post_id: post id
        :return: 20 comments associated with a post
        '''

        return Comment.all().filter("post_id =", post_id).fetch(20)
