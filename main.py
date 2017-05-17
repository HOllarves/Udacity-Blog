import os
from Models.User import User
from Models.Post import Post
from Models.Comment import  Comment
import webapp2
import jinja2
from cookies import CookieHandler
from validation import Validation
import decorators

template_dir = os.path.join(os.path.dirname(__file__))
theme_dir = os.path.join(os.path.dirname(__file__), 'theme')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader([template_dir, theme_dir]),
                               autoescape = True)

class BaseHandler(webapp2.RequestHandler):

    """
    Basic operations for all pages.
    Authentication, cookie handling and
    rendering.
    """

    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))


    def write(self, *a, **kw):

        '''
        Renders plain text
        :param a: text
        :param kw: other parameters
        '''

        self.response.out.write(*a, **kw)


    def set_secure_cookie(self, name, val):

        '''
        Creates a secure cookie
        :param name: cookie name
        :param val: cookie value
        :return: Sets the appropiate header
        '''

        cookie_val = CookieHandler.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))


    def read_secure_cookie(self, name):

        '''
        Validates the authenticity of a cookie
        :param name: cookie name to be validated
        :return: authenticity of the cookie. True or False
        '''

        cookie_val = self.request.cookies.get(name)
        return cookie_val and CookieHandler.check_secure_val(cookie_val)

    def login(self, user):

        '''
        Logs in the user (Sets the appropiate cookies)
        :param user object
        :return: Sets the appropiate secure cookies
        '''

        self.set_secure_cookie('user_id', str(user.key().id()))
        self.set_secure_cookie('user_name', str(user.username))

    def logout(self):

        '''
        Remove cookies
        :return: Sets the appropiate headers
        '''

        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')
        self.response.headers.add_header('Set-Cookie', 'user_name=;Path=/')

    def valid_user(self):

        '''
        Validates that the user making a request is a valid user
        :return: True if user is valid. Else, None
        '''

        username_cookie = self.request.cookies.get('user_name')
        user_id_cookie = self.request.cookies.get('user_id')
        if username_cookie and user_id_cookie and CookieHandler.check_secure_val(username_cookie) and CookieHandler.check_secure_val(user_id_cookie):
            return True

    def get_username(self):

        '''
         Retrives username from cookie
        '''

        if self.request.cookies.get('user_name'):
            return self.request.cookies.get('user_name').split('|')[0]

    def get_user_id(self):

        '''
        Retrives user_id from cookie
        '''
        if self.request.cookies.get('user_id'):
            return self.request.cookies.get('user_id').split('|')[0]

    def format_content(self, content):

        '''
        Replaces new lines with <br> for 
        poper HTML rendering
        :param content: text to be formatted
        :return: Formatted content 
        '''

        return content.replace('\n', '<br>')

    def reformat_content(self, content):

        '''
        Returns post content to it's previous state.
        Changing <br> with new lines
        :param content: text to be formatted 
        :return: Formatted content
        '''

        return content.replace('<br>', '\n')



class Home(BaseHandler):

    '''
    Home page
    template: theme/home.html
    '''

    def get(self):
        username = None
        if (self.valid_user()):
            username_cookie = self.request.cookies.get('user_name')
            username = username_cookie.split('|')[0]

        posts_query = Post.all().order('-created_at')
        posts = posts_query.fetch(10)
        self.render("home.html", username=username, posts=posts)

class Signup(BaseHandler):

    '''
    Sign Up Page
    template: theme/sign-up.html
    '''

    def get(self):
        self.render("sign-up.html")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        params = dict(username = username,
                      email = email)

        # Validating all fields
        if not Validation.valid_username(username):
            params["error_username"] = "That's not a valid username."
            have_error = True

        if not Validation.valid_password(password):
            params["error_password"] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params["error_verify"] = "Your passwords didn't match."
            have_error = True

        if not Validation.valid_email(email):
            params["error_email"] = "That's not a valid email."
            have_error = True
        if User.get_by_name(username):
            params["user_taken"] = "This username is already taken"
            have_error = True

        if have_error:
            self.render("sign-up.html", **params)
        else:
            # Creates new user
            new_user = User.register(username, password, email)
            new_user.put()
            self.login(new_user)
            self.redirect("/")

class Login(BaseHandler):

    '''
    Login Page
    template: theme/login.html
    '''

    def get(self):
        if self.request.cookies.get("user_name"):
            self.redirect("/")
        else:
            self.render("login.html")

    def post(self):
        have_error = False
        username = self.request.get("username")
        password = self.request.get("password")

        params = dict(error_username = None,
                      error_password = None)

        # Validates fields
        if not Validation.valid_username(username):
            params["error_username"] = "That's not a valid username."
            have_error = True

        if not Validation.valid_password(password):
            params["error_password"] = "That wasn't a valid password."
            have_error = True

        if have_error:
            self.render("login.html", **params)
        else:
            # Login user
            log_user = User.login(username, password)
            if log_user:
                self.login(log_user)
                self.redirect("/")
            else:
                self.render("login.html", credential_error="There seems to be an error with your credentials, please check")

class Logout(BaseHandler):

    '''
    Logout handler
    '''

    def get(self):
        if self.valid_user():
            self.logout()
            self.redirect('/')
        else:
            self.redirect('/')


class Posts(BaseHandler):

    '''
    Posts Page
    template: theme/new-post.html
    '''

    def get(self):
        if self.valid_user():
            username = self.get_username()
            self.render("new-post.html", username=username)
        else:
            self.redirect('/login')

    def post(self):
        if self.valid_user():
            have_error = False
            params = dict(error_title=None,
                          error_content=None)

            user_id = self.get_user_id()
            author = self.get_username()
            title = self.request.get("title")
            content = self.request.get("content")

            # Validating post fields
            if not Validation.valid_title(title):
                have_error = True
                params["error_title"] = "Title is too small"

            if not Validation.valid_content(content):
                have_error = True
                params["error_content"] = "Content is too small"

            if have_error:
                self.render("new-post.html", **params)
            else:
                # Formatting content and saving post
                formatted_content = self.format_content(content)
                new_post = Post.add(user_id, author, title, formatted_content)
                new_post.put()
                self.redirect('/articles/%s' % str(new_post.key().id()))


class DeletePost(BaseHandler):

    '''
    Delete Post Handler
    '''
    @decorators.is_users_post
    def get(self, post_id):
        if self.valid_user():
            post = Post.get_post(post_id)
            post.delete()
            self.redirect('/')
        else:
            self.redirect('/login')

class EditPost(BaseHandler):

    '''
    Edit post handler
    template: theme/edit-post
    '''

    @decorators.is_users_post
    def get(self, post_id):
        if self.valid_user():
            username = self.get_username()
            post = Post.get_post(post_id)
            post.content = self.reformat_content(post.content)
            self.render("edit-post.html", post=post, username=username)
        else:
            self.redirect('/login')

    @decorators.is_users_post
    def post(self, post_id):
        if self.valid_user():
            have_error = False
            params = dict(error_title=None,
                          error_content=None)

            post = Post.get_post(post_id)
            title = self.request.get("title")
            content = self.request.get("content")
            # Validating post fields
            if not Validation.valid_title(title):
                have_error = True
                params["error_title"] = "Title is too small"

            if not Validation.valid_content(content):
                have_error = True
                params["error_content"] = "Content is too small"
            if have_error:
                post.content = self.reformat_content(post.content)
                params["post"] = post
                self.render("edit-post.html",  **params)
            else:
                post.title = title
                post.content = self.format_content(content)
                post.put()
                self.redirect('/articles/%s' % post_id)
        else:
            self.redirect('/login')



class Articles(BaseHandler):

    '''
    Articles Page
    template: theme/post.html
    '''

    @decorators.post_exists
    def get(self, post_id):
        username = self.get_username()
        user_id = self.get_user_id()
        post = Post.get_post(post_id)
        comments = Comment.by_post_id(post_id)
        self.render("post.html", post=post, username=username, comments=comments, user_id=user_id)


class Comments(BaseHandler):

    '''
    Comments Handler
    '''

    @decorators.post_exists
    def post(self, post_id):
        if self.valid_user():
            content = self.request.get("comment")
            username = self.get_username()
            user_id = self.get_user_id()
            new_comment = Comment.add(username=username, u_id=user_id, p_id=post_id.strip(), content=content)
            new_comment.put()
            self.redirect('/articles/%s' % post_id)
        else:
            self.redirect('/login')




class DeleteComment(BaseHandler):

    @decorators.is_user_comment
    def get(self, comment_id):
        comment = Comment.get_comment(comment_id)
        post_id = comment.post_id
        if self.valid_user():
            comment.delete()
            self.redirect('/articles/%s' % post_id)
        else:
            self.redirect('/login')

class EditComment(BaseHandler):

    @decorators.is_user_comment
    def get(self, comment_id):
            comment = Comment.get_comment(comment_id)
            if self.valid_user():
                comments = Comment.by_post_id(comment.post_id)
                post = Post.get_post(comment.post_id)
                username = self.get_username()
                user_id = self.get_user_id()
                self.render("post.html", post=post, username=username, comments=comments, user_id=user_id, edit_comment=True)
            else:
                self.redirect('/articles/%s' % comment.post_id)

    @decorators.is_user_comment
    def post(self, comment_id):
        comment = Comment.get_comment(comment_id)
        if self.valid_user():
            new_comment = self.request.get("comment")
            comment.content = new_comment
            comment.put()
            self.redirect('/articles/%s' % comment.post_id)
        else:
            self.redirect('/articles/%s' % comment.post_id)


class UpVotes(BaseHandler):

    '''
    Up Vote handler
    '''

    @decorators.can_vote
    def get(self, post_id):
        if self.valid_user():
            post = Post.get_post(post_id)
            post.add_up_vote()
            user = User.get(self.get_user_id())
            user.add_vote(post_id)
            self.redirect('/articles/%s' % post_id)
        else:
            self.redirect('/login')

class DownVote(BaseHandler):

    '''
    Down Vote Handler
    '''

    @decorators.can_vote
    def get(self, post_id):
        if self.valid_user():
            post = Post.get_post(post_id)
            post.add_down_vote()
            user = User.get(self.get_user_id())
            user.add_vote(post_id)
            self.redirect('/articles/%s' % post_id)
        else:
            self.redirect('/login')


# Defining routes and mapping to classes/handlers

app = webapp2.WSGIApplication([('/', Home),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/posts', Posts),
                               ('/posts/delete/([0-9]+)', DeletePost),
                               ('/posts/edit/([0-9]+)', EditPost),
                               ('/articles/([0-9]+)', Articles),
                               ('/comments/([0-9]+)', Comments),
                               ('/comments/delete/([0-9]+)', DeleteComment),
                               ('/comments/edit/([0-9]+)', EditComment),
                               ('/upvote/([0-9]+)', UpVotes),
                               ('/downvote/([0-9]+)', DownVote)],
                              debug=True)

