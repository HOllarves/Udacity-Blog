from Models.Post import  Post
from Models.Comment import Comment
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
    Method decorator that checks if a post belongs to a user before allowing
    the process to be executed.
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
    Method decorator that checks if a user owns a specific comment
    :param f: 
    :return: 
    '''

    @wraps(f)
    def check_is_user_comment(self, c_id):
        user_id = self.get_user_id()
        comment = Comment.get_comment(c_id)
        if user_id == comment.user_id:
            return f(self, c_id)
        else:
            self.redirect('/login')
            return
    return check_is_user_comment

def comment_exists(f):

    '''
    Method that checks that a specific comment exists
    :param f: decorated function
    :return: decorated function
    '''

    @wraps(f)
    def check_comment_exists(self, c_id):
        comment = Comment.get_comment(c_id)
        if comment:
            return f(self, c_id)
        else:
            self.redirect('/')
            return
    return check_comment_exists