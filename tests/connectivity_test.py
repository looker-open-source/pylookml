import unittest, copy
import lookml.lookml as lookml
import lkml as lkml
from pprint import pprint
import configparser, json
# from looker_sdk import client, models, methods

from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('settings.ini')

class testConnectivity(unittest.TestCase):
    '''
        objective: 
            Test coverage on all the methods of interacting with external services
            github (access_token)
            ssh git interaction
            Local filesystem
            Looker API 
            Looker deploy webhook
            success criteria: 
            need to successfully connect, perform multiple operations CRUD, then reconnect and parse again
    '''
    def setUp(self):
        pass

    def test_local_filesystem(self):
        pass
    def test_github_connection(self):
        pass
    def test_ssh_git_connection(self):
        pass
    def test_looker_api(self):
        pass
    def test_looker_deploy_webhook(self):
        pass

    def tearDown(self):
        pass
