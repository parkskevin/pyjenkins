#!/usr/bin/env python

import json
import urllib2
import unittest
import argparse
import unittest
import sys

sys.path.insert(1, '/home/kevin/google_appengine')
sys.path.insert(1, '/home/kevin/google_appengine/lib/yaml/lib')
sys.path.insert(1, '/home/kevin/Desktop/pyjenkins/app')
from google.appengine.ext import testbed
from google.appengine.api import memcache
from google.appengine.ext import ndb
from randomuser import *

class TestPutRandomUser(unittest.TestCase):
    def setUp(self):
        # code from https://cloud.google.com/appengine/docs/python/tools/localunittesting?hl=en
        # First, create an instance of the Testbed class.
        self.testbed = testbed.Testbed()
        # Then activate the testbed, which prepares the service stubs for use.
        self.testbed.activate()
        # Next, declare which service stubs you want to use.
        self.testbed.init_datastore_v3_stub()
        self.testbed.init_memcache_stub()
        # Clear ndb's in-context cache between tests.
        # This prevents data from leaking between tests.
        # Alternatively, you could disable caching by
        # using ndb.get_context().set_cache_policy(False)
        ndb.get_context().clear_cache()

    def testPutTest(self):
        # perform query, sort with latest at 0, compare data to make sure it matches
        person = RandomUser(name='Test Smith', email='ts@example.com', username='tsmith', picture='http://www.picture.com')
        person.putPerson()
        results = TestPerson.query().fetch(1)
        self.assertEqual(results[0].name, person.name)
        self.assertEqual(results[0].username, person.username)
        self.assertEqual(results[0].email, person.email)
        self.assertEqual(results[0].picture, person.picture)

    def tearDown(self):
        self.testbed.deactivate()


suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestPutRandomUser))
runner = unittest.TextTestRunner(verbosity=2)
# http://stackoverflow.com/questions/24972098/unit-test-script-returns-exit-code-0-even-if-tests-fail
ret = not runner.run(suite).wasSuccessful()
sys.exit(ret)

