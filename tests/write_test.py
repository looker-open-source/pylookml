import lookml.lookml as lookml
import unittest
import lkml as lkml
from pprint import pprint

class testWriting(unittest.TestCase):
    '''
        Objective / coverage
          Read all file types from filesystem: 
            model, 
            view, 
            other lkml files, 
            manifest, 
            dashboard, 
            js, 
            json, 
            maplayer
            Success Criteria:
                need coverage of all basic operations: mutating each sub property and asserting the effect
                novel convenience methods should be covered in test cases
                written object needs to be reparsible to pass
    '''
    def setUp(self):
        pass

    #basic objects
    def test_model_file(self):
        pass
    def test_view_file(self):
        pass
    def test_other_lkml_file(self):
        pass
    def test_manifest_file(self):
        pass
    def test_dashboard_file(self):
        pass
    def test_js_file(self):
        pass
    def test_json_file(self):
        pass
    def test_maplayer_topojson(self):
        pass

    #syntax constructs
    def test_refinements(self):
        pass
    def test_extensions(self):
        pass
    def test_dimension(self):
        pass
    def test_measure(self):
        pass

    def tearDown(self):
        pass
