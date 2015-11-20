from google.appengine.ext import ndb


class RandomUser(object):
    def __init__(self, name, email, username, picture):
        self.name = name
        self.email = email
        self.username = username
        self.picture = picture

    def __getitem__(self, item):
        if item == 'name':
            return self.name
        elif item == 'email':
            return self.email
        elif item == 'username':
            return self.username
        elif item == 'picture':
            return self.picture
        else:
            return None

    def putPerson(self):
        root = TestPersonRoot(id='root')
        ndbPerson = TestPerson(parent=root.key)
        try:
            ndbPerson.name = self.name
            ndbPerson.email = self.email
            ndbPerson.username = self.username
            ndbPerson.picture = self.picture
            ndbPerson.put()
        except Exception as e:
            raise e


# adapted from https://cloud.google.com/appengine/docs/python/tools/localunittesting?hl=en
class TestPerson(ndb.Model):
    """
    Model class used to demonstrate testing
    """
    name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    username = ndb.StringProperty(required=True)
    picture = ndb.StringProperty(required=True)
    date = ndb.DateTimeProperty(auto_now_add=True)


class TestPersonRoot(ndb.Model):
    pass
