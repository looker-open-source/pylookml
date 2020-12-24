import unittest, copy
import lookml
import lkml as lkml
from pprint import pprint
import configparser, json
# from looker_sdk import client, models, methods

from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('settings.ini')

class testScenariosDeployExtension(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        pass
    def test_deploy_extension(self):
        #deploy a parametarized extension
        pass

