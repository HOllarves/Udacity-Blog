from google.appengine.ext import db

class Post(db.Model):
    user_id = db.StringProperty(required = True)
    author = db.StringProperty(required = True)
    title = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created_at = db.DateTimeProperty(auto_now_add = True)
    up_votes = db.IntegerProperty(default = 0)
    down_votes = db.IntegerProperty(default = 0)
    last_modified = db.DateTimeProperty(auto_now = True)
    last_vote = db.DateTimeProperty(default = None)

    def add_up_vote(self):
        self.up_votes += 1
        self.put()

    def add_down_vote(self):
        self.down_votes  += 1
        self.put()

    @classmethod
    def get_post(cls, p_id):
        key = db.Key.from_path('Post', int(p_id))
        return db.get(key)

    @classmethod
    def add(cls, user_id, author, title, content):
        return Post(user_id=user_id, author=author, title=title, content=content)