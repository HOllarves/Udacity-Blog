from google.appengine.ext import db

class Comment(db.Model):
    username = db.StringProperty(required = True)
    user_id = db.StringProperty(required = True)
    post_id = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_at = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def get_comment(cls, c_id):
        key = db.Key.from_path('Comment', int(c_id))
        return db.get(key)

    @classmethod
    def add(cls, username, u_id, p_id, content):
        return Comment(username= username, user_id=u_id, post_id=p_id, content=content)

    @classmethod
    def by_post_id(cls, post_id):
        return Comment.all().filter("post_id =", post_id).fetch(20)
