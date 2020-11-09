import unittest, copy
import lookml
import lkml as lkml
from pprint import pprint
import configparser, json
# from looker_sdk import client, models, methods

from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('settings.ini')



class testScenarios(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        pass
    def test_eav_unnester(self):
        pass
    def test_deploy_extension(self):
        #deploy a parametarized extension
        pass
    def test_generate_aggregate_table(self):
        #loop through an aggregate awareness scenario
        pass
    def test_tuning_whitespace(self):
        #once it's parameterizable
        pass
    
    def test_generating_lookml_from_schema(self):
        pass

    def test_replacing_child_and_ancestor_references(self):
        pass

    def tearDown(self):
        pass

