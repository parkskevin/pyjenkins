#!/usr/bin/env python

import json
import urllib2
import unittest
import argparse
import unittest
import sys
import os

sys.path.insert(1, '/home/kevin/google_appengine')
sys.path.insert(1, '/home/kevin/google_appengine/lib/yaml/lib')
sys.path.insert(1, os.getcwd() + '/../app')
from randomuser import *

cloudHost = 'http://pyjenkins-1132.appspot.com'
localHost = 'http://localhost'

# cmd line parsing to determine which host to test against
parser = argparse.ArgumentParser(description="testonline")
parser.add_argument('--host', choices=['local', 'cloud'], required=True)
parser.add_argument('--port', type=int, default=80)
args = parser.parse_args()

host = args.host
if host == 'local':
    host = localHost
elif host == 'cloud':
    host = cloudHost
port = args.port


class TestPutRandomUser(unittest.TestCase):
    def testKeysReturn(self):
        # make the get request and capture JSON return data
        parsed_person = json.load(urllib2.urlopen('{0}:{1}'.format(host, port)))
        validkeys = ['username', 'email', 'name', 'picture']
        testkeys = []
        for i in parsed_person.iterkeys():
            testkeys.append(i)
        self.assertItemsEqual(validkeys, testkeys)


suite = unittest.TestSuite()
suite.addTests(unittest.makeSuite(TestPutRandomUser))
runner = unittest.TextTestRunner(verbosity=2)
# http://stackoverflow.com/questions/24972098/unit-test-script-returns-exit-code-0-even-if-tests-fail
ret = not runner.run(suite).wasSuccessful()
sys.exit(ret)
