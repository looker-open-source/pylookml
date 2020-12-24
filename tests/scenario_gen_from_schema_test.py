import unittest, copy
import lookml
import lkml as lkml
from pprint import pprint
import configparser, json
# from looker_sdk import client, models, methods

from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('settings.ini')



class testScenariosGenerateFromSchema(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        pass
    
    def test_generating_lookml_from_schema(self):
        pass

    def tearDown(self):
        pass

