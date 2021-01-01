
import src.lookml.lookml as lookml
import src.lookml.lkml as lkml

import unittest, copy
from pprint import pprint
import configparser, json
from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('tests/settings.ini')

class testScenariosDeployExtension(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        pass
    def test_deploy_extension(self):
        #deploy a parametarized extension
        pass

