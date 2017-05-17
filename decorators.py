from Models.Post import  Post
from Models.Comment import Comment
from Models.User import User
from functools import wraps

def post_exists(f):

    '''
    Thanks for introducing me to decorators. Let me explain what I've learnt from them.
    Decorators basically change the behaviour of a function, method or a class by adding extra
    steps or completely different ones to the execution of a function or a class.
    In this case, the decorator takes the function decorated as a parameter, checks if a the post exists
    and if so, allows the function to be executed. Else, it redirects to the homepage.
    :param f: decorated function
    :return: decorated function.
    '''

    #This is decorator-sception
    @wraps(f)
    def check_existence(self, post_id):
        post = Post.get_post(post_id)
        if post:
            return f(self, post_id)
        else:
            self.redirect('/')
            return
    return check_existence

def is_users_post(f):

    '''
    Method decorator that checks if a post exists and
    belongs to the user
    :param f: decorated function
    :return: decorated function.
    '''

    @wraps(f)
    def check_is_users_post(self, post_id):
        user_id = self.get_user_id()
        post = Post.get_post(post_id)
        if post and post.user_id == user_id:
            return f(self, post_id)
        else:
            self.redirect('/login')
            return
    return check_is_users_post

def is_user_comment(f):

    '''
    Method decorator that checks if a comment exists
    and the user owns it
    :param f: 
    :return: 
    '''

    @wraps(f)
    def check_is_user_comment(self, c_id):
        user_id = self.get_user_id()
        comment = Comment.get_comment(c_id)
        if comment and user_id == comment.user_id:
            return f(self, c_id)
        else:
            self.redirect('/login')
            return
    return check_is_user_comment

def can_vote(f):

    '''
    Method decorator that checks if a post exists 
    and that a user can vote in it
    :param f: decorated function
    :return: decorated function
    '''

    @wraps(f)
    def check_can_vote(self, p_id):
        post = Post.get_post(p_id)
        user_id = self.get_user_id()
        user = User.get(user_id)
        if post and  post.user_id != str(user.key().id()):
            if len(user.liked_posts) == 0:
                return f(self, p_id)
            else:
                for i in user.liked_posts:
                    if i == p_id:
                        self.render('post.html', post=post, username=user.username, error="It looks you already voted in this post")
                        return
                    if i == user.liked_posts[-1]:
                        return f(self, p_id)
        else:
            self.render('post.html', post=post, username=user.username, error="Can't vote on your own post")
    return check_can_vote