#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import cgi
# from http://stackoverflow.com/questions/2817481/how-do-i-request-and-process-json-with-python
import json
import urllib2
import datetime
import os


class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("""
            <!DOCTYPE html>
              <head>
                <title>RandomUser</title>
              <body>
                <form action="randomUser" method="post">
                  <div>
                    Click <a href=\"/randomuser\">HERE</a> to Get Random Person Data!<br>
                  </div>
                </form>
              </body>
            </html>
        """)


class RandomUser(webapp2.RequestHandler):
    page = u'''
<!DOCTYPE html>
  <head>
    <title>RandomUser</title>
  </head>
  <body>
    <h2>Random \"Person\" Data:</h2>
    <b>Name: </b>{name}<br>
    <b>Email: </b>{email}<br>
    <b>Username: </b>{username}<br>
    <b>Image: </b><img src=\"{picture}\" alt=pic><br>
    <b>Generated: </b>{time}<br>
    <a href=\"http://randomuser.me\">http://randomuser.me</a>
    <form action=\"/randomuser\" method=\"get\">
      <input type=\"submit\" value=\"Again!\">
    </form>
  </body>
</html>'''

    def get(self):
        # from http://stackoverflow.com/questions/2817481/how-do-i-request-and-process-json-with-python
        # make http request from url, return json, store in variable
        parsed_data = json.load(urllib2.urlopen('http://randomuser.me/api/?format=json'))
        # parse the json using the imported json library according to
        # http://docs.python-guide.org/en/latest/scenarios/json/
        person = self.makePerson(parsed_data)
        time = unicode(self.getTime())
        name = unicode(person['name'])
        email = unicode(person['email'])
        username = unicode(person['username'])
        picture = unicode(person['picture'])
        #format page like http://anh.cs.luc.edu/python/hands-on/3.1/handsonHtml/webtemplates.html
        contents = self.page.format(**locals())
        self.response.out.write(contents)

    def makePerson(self, parsed_data):
        firstPerson = parsed_data['results'][0]['user']
        person = {
            'name': (firstPerson['name']['first'] + ' ' + firstPerson['name']['last']),
            'email': firstPerson['email'],
            'username': firstPerson['username'],
            'picture': firstPerson['picture']['thumbnail']
        }
        return person

    def getTime(self):
        currentTimeDate = datetime.datetime.now()
        return (currentTimeDate.strftime("%m/%d/%Y %H:%M:%S %p") + ' ' + os.environ['TZ'])


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/randomuser', RandomUser)
], debug=True)


def main():
    app.run()


if __name__ == "__main__":
    main()
