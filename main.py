import os
from datetime import datetime, timedelta
from Models.User import User
from Models.Post import Post
from Models.Comment import  Comment
import webapp2
import jinja2
from cookies import CookieHandler
from validation import Validation

template_dir = os.path.join(os.path.dirname(__file__))
theme_dir = os.path.join(os.path.dirname(__file__), 'theme')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader([template_dir, theme_dir]),
                               autoescape = True)

class BaseHandler(webapp2.RequestHandler):

    @staticmethod
    def render_str(template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def set_secure_cookie(self, name, val):
        cookie_val = CookieHandler.make_secure_val(val)
        self.response.headers.add_header('Set-Cookie', '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and CookieHandler.check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
        self.set_secure_cookie('user_name', str(user.username))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=;Path=/')

    def valid_user(self):
        username_cookie = self.request.cookies.get('user_name')
        user_id_cookie = self.request.cookies.get('user_id')
        if username_cookie and user_id_cookie and CookieHandler.check_secure_val(username_cookie) and CookieHandler.check_secure_val(user_id_cookie):
            return True

    def get_username(self):
        return self.request.cookies.get("user_name").split('|')[0]

    def get_user_id(self):
        return self.request.cookies.get('user_id').split('|')[0]

    def format_content(self, content):
        return content.replace('\n', '<br>')

    def reformat_content(self, content):
        return content.replace('<br>', '\n')

    def is_users_post(self, p_id):
        p = Post.get_post(p_id)
        if p.author == self.get_username() and p.user_id == self.get_user_id():
            return True



class Home(BaseHandler):

    def get(self):
        username = None
        if (self.valid_user()):
            username_cookie = self.request.cookies.get('user_name')
            username = username_cookie.split('|')[0]

        posts_query = Post.all().order('-created_at')
        posts = posts_query.fetch(10)
        self.render("home.html", username=username, posts=posts)

class Signup(BaseHandler):

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
            new_user = User.register(username, password, email)
            new_user.put()
            self.login(new_user)
            self.redirect("/")

class Login(BaseHandler):

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

        if not Validation.valid_username(username):
            params["error_username"] = "That's not a valid username."
            have_error = True

        if not Validation.valid_password(password):
            params["error_password"] = "That wasn't a valid password."
            have_error = True

        if have_error:
            self.render("login.html", **params)
        else:
            log_user = User.login(username, password)
            if log_user:
                self.login(log_user)
                self.redirect("/")
            else:
                self.render("login.html", credential_error="There seems to be an error with your credentials, please check")


class Posts(BaseHandler):

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

            if not Validation.valid_title(title):
                have_error = True
                params["error_title"] = "Title is too small"

            if not Validation.valid_content(content):
                have_error = True
                params["error_content"] = "Content is too small"

            if have_error:
                self.render("new-post.html", **params)
            else:
                formatted_content = self.format_content(content)
                new_post = Post.add(user_id, author, title, formatted_content)
                new_post.put()
                self.redirect('/articles/%s' % str(new_post.key().id()))


class DeletePost(BaseHandler):
    def get(self):
        p_id = self.request.get("post_id")
        if self.valid_user():
            if self.is_users_post(p_id):
                post = Post.get_post(p_id)
                post.delete()
                self.redirect('/')
        else:
            self.redirect('/')

class EditPost(BaseHandler):

    def get(self):
        if self.valid_user():
            username = self.get_username()
            p_id = self.request.get("post_id")
            post = Post.get_post(p_id)
            post.content = self.reformat_content(post.content)
            self.render("edit-post.html", post=post, username=username)
        else:
            self.redirect('/')

    def post(self):
        if self.valid_user():
            p_id = self.request.get("post_id")
            title = self.request.get("title")
            content = self.request.get("content")
            post = Post.get_post(int(p_id))
            post.title = title
            post.content = self.format_content(content)
            post.put()
            self.redirect('/articles/%s' % p_id)
        else:
            self.redirect('/')



class Articles(BaseHandler):

    def get(self, p_id):
        username = self.get_username()
        user_id = self.get_user_id()
        post = Post.get_post(p_id)
        comments = Comment.by_post_id(p_id)
        print comments
        self.render("post.html", post=post, username=username, comments=comments, user_id=user_id)

class Comments(BaseHandler):

    def post(self):
        if self.valid_user():
            post_id = self.request.get("post_id")
            content = self.request.get("comment")
            username = self.get_username()
            user_id = self.get_user_id()
            new_comment = Comment.add(username=username, u_id=user_id, p_id=post_id.strip(), content=content)
            new_comment.put()
            self.redirect('/articles/%s' % post_id)
        else:
            post_id = self.request.get("post_id")
            self.render('/articles/%s' % post_id, auth_error="You must be logged in to comment on a post")


class UpVotes(BaseHandler):

    def get(self):
        if self.valid_user():
            post_id = self.request.get('post_id')
            post = Post.get_post(post_id)
            username = self.get_username()
            comments = Comment.by_post_id(post_id)
            user_id = self.get_user_id()
            print
            if post.last_vote == None:
                post.last_vote = datetime.utcnow()
                post.add_up_vote()
                self.redirect('/articles/%s' % post_id)
            elif (datetime.utcnow() - post.last_vote) > timedelta(1):
                post.add_up_vote()
                post.last_vote = datetime.utcnow()
                self.redirect('/articles/%s' % post_id)
            else:
                self.render("post.html", post=post, username=username, comments=comments, user_id=user_id, error="You already voted today")

        else:
            self.redirect('/')

class DownVote(BaseHandler):

    def get(self):
        if self.valid_user():
            post_id = self.request.get('post_id')
            username = self.get_username()
            comments = Comment.by_post_id(post_id)
            user_id = self.get_user_id()
            post = Post.get_post(post_id)
            if (datetime.utcnow() - post.last_vote) > timedelta(1):
                post.add_down_vote()
                self.redirect('/articles/%s' % post_id)
            else:
                self.render("post.html", post=post, username=username, comments=comments, user_id=user_id, error="You already voted today")
        else:
            self.redirect('/')

app = webapp2.WSGIApplication([('/', Home),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/posts', Posts),
                               ('/posts/delete', DeletePost),
                               ('/posts/edit', EditPost),
                               ('/articles/([0-9]+)', Articles),
                               ('/comments', Comments),
                               ('/upvote', UpVotes),
                               ('/downvote', DownVote)],
                              debug=True)