#!/usr/bin/env python

import webapp2
import json
import urllib2
from randomuser import *


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # from http://stackoverflow.com/questions/2817481/how-do-i-request-and-process-json-with-python
        # make http request from url, return json, store in variable
        parsed_data = json.load(urllib2.urlopen('http://randomuser.me/api/?format=json'))
        # parse the json and make a person
        person = self.makePerson(parsed_data)
        # save the person to datastore
        person.putPerson()
        # write out the json of the person
        self.response.write(json.dumps(person.__dict__))

    def makePerson(self, parsed_data):
        firstPerson = parsed_data['results'][0]['user']
        person = {
            'name': (firstPerson['name']['first'] + ' ' + firstPerson['name']['last']),
            'email': firstPerson['email'],
            'username': firstPerson['username'],
            'picture': firstPerson['picture']['thumbnail']
        }
        return RandomUser(**person)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)


def main():
    app.run()


if __name__ == "__main__":
    main()
