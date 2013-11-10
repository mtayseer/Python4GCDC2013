import webapp2, jinja2, os

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class Garbage(ndb.Model):
    name = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    author = ndb.UserProperty()
    position = ndb.GeoPtProperty()

class MainPage(webapp2.RequestHandler):

    def get(self):
        template = JINJA_ENVIRONMENT.get_template('home.html')

        # Write the submission form and the footer of the page
        self.response.write(template.render({
                            'user': users.get_current_user(),
                            'garbage_marks': Garbage.query().fetch(10),
                            'login_url': users.create_login_url(self.request.uri),
                            'logout_url': users.create_logout_url(self.request.uri)
                            }))


class AddGarbageMark(webapp2.RequestHandler):
    def get(self):
        if self.request.get('name') and self.request.get('lat') and self.request.get('lng'):
            mark = Garbage(author=users.get_current_user(), 
                           name=self.request.get('name'), 
                           position=ndb.GeoPt(lat=self.request.get('lat'), lon=self.request.get('lng')))
            mark.put()
            self.response.write('{"result": "Success"}')
        else:
            self.response.write('{"result": "Fail"}')

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/add', AddGarbageMark)
], debug=True)