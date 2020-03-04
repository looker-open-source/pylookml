import unittest, copy
import lookml
import configparser
config = configparser.ConfigParser()
config.read('lookml/tests/settings.ini')

#TODO: Define Essential Test Suite:
    # create "kitchen sink" model file with every obscure problematic parameter, fetch it from a project parse everything, put it back, parse it again.
    # Do this for raw filesytem level stuff, and for github based projects. 
#TODO: Add test coverage for providing positional arguments of vastly different types, i.e. lookml class vs json etc. 

class testKitchenSinkLocal(unittest.TestCase):
    '''
        Test Procedure:
        Setup) Obtain Local Kitchen Sink Model File
        2) Parse the file
        3) Run a few assertions that are facts of the file
            A) loop over loopable constructs. You know for example there are 3 tags in foo
            B) Assert Dimension length, measure length, etc
        4) Assert exceptions when trying to do disallowed operations? (anoying interaction with the debugger)
        5) Make [A,B,C] modifications to the fileObject and save it as a newfile / overwrite KitchenSink2
            A) Add each type of field
            B) Add a tag, suggestions, drill_fields, set, action, multiple links etc
            C) Add an additional view
            D) Add an NDT
        6) Fetch and parse KitchenSink2
        7) Run assertions that confirm [A,B,C,D] were successfully applied
        TearDown)  remove KitchenSink2 if it exists (comment out if having parse difficulties)
    '''
# @unittest.skipIf(condition, reason)
# @unittest.expectedFailure

    def setUp(self):
        self.f = lookml.File('lookml/tests/kitchenSink/kitchenSink.model.lkml')
        self.f2 = None
        self.order_items = self.f.views.order_items
        self.order_items_explore = self.f.explores.order_items

    def test_step2(self):
        '''
            2) Parse the file
        '''
        pass

    def test_step3a(self):
        '''
            3) Run a few assertions that are facts of the file
            A) loop over loopable constructs. You know for example there are 3 tags in foo
        '''
        #46 total
        self.totalFields = len(self.order_items)
        # 17 Dimensions
        self.totalDims = len(list(self.order_items.dims()))
        # 5  DimensionGroups
        self.totalDgs = len(list(self.order_items.dimensionGroups()))
        # 22 Measures
        self.totalMeas = len(list(self.order_items.measures()))
        # 2  Filters
        self.totalFilters = len(list(self.order_items.filters()))
        # 0  Paramters
        self.totalParams = len(list(self.order_items.parameters()))
        # print(self.order_items.foo)
        
        #Asserts all the subtypes of fields should add up to the total
        self.assertEqual(self.totalFields,
              self.totalDims
            + self.totalDgs
            + self.totalMeas
            + self.totalFilters 
            + self.totalParams
            )
        self.assertEqual(len(self.order_items),len(list(self.order_items.fieldNames()))) 
        self.assertEqual(len(self.order_items),47) #Counts the total fields

        self.assertTrue(isinstance(self.order_items.id,lookml.Dimension))
        self.assertTrue(isinstance(self.order_items.total_gross_margin,lookml.Measure))
        self.assertTrue(isinstance(self.order_items.cohort_by,lookml.Filter))
        self.assertTrue(isinstance(self.order_items.foo,lookml.Parameter))

        #Check field level list constructs
        self.assertTrue("abc" in self.order_items.id.required_access_grants)
        self.assertTrue(1 == len(self.order_items.id.required_access_grants))

        self.assertTrue("a" in self.order_items.id.tags)
        self.assertTrue(3 == len(self.order_items.id.tags))

        self.assertTrue("suggestion1" in self.order_items.id.suggestions)
        self.assertTrue(2 == len(self.order_items.id.suggestions))
        
        #Primary Key Checks
        self.assertEqual(self.order_items.primaryKey, 'id')
        self.assertEqual(self.order_items.primaryKey, self.order_items.pk.name)
        
        #Check Children
        self.assertEqual(1, len(list(self.order_items.shipping_time.children())))

        # Check Looping construct
        for tag in self.order_items.id.tags:
            pass

        for tag in self.order_items.id.suggestions:
            pass

    def test_step3b(self):
        '''
            3) Run a few assertions that are facts of the file
            B) ssert Dimension length, measure length, etc
        '''
        pass

    def test_step4(self):
        '''
            4) Assert exceptions when trying to do disallowed operations? (anoying interaction with the debugger)
        '''
        #TODO: add more exception handling / raise more errors in the code (V2?)
        with self.assertRaises(KeyError):
            #the field fake does not exist
            self.order_items.getField('fake')

    def test_step5(self):
        '''
            5) Make [A,B,C] modifications to the fileObject and save it as a newfile / overwrite KitchenSink2
                A) Add each type of field
                B) Add a tag, suggestions, drill_fields, set, action, multiple links etc
                C) Add an additional view
                D) Add an NDT
        '''
        self.f_copy = copy.copy(self.f)
        #### Modifications ###
        self.f_copy.views.order_items.id.sql = "${TABLE}.test_sql_change"
        self.f_copy.views.order_items + 'test_add_dimension'
        self.f_copy.views.order_items.shipping_time.change_name_and_child_references('time_in_transit')
        #Check tag addition and subtraction
        self.f_copy.views.order_items.id.addTag('x')
        self.assertEqual(len(self.f_copy.views.order_items.id.tags),4)
        self.f_copy.views.order_items.id.tags - 'x'
        self.assertEqual(len(self.f_copy.views.order_items.id.tags),3)
        #TODO: Check sql addition functions
        # test1.foo.sql_nvl("0")
        #TODO: implement a join and check in validation step
        #look up an explore
        # mf.explores.test1.test2.on(
        #         vf.views.test1.foo,'=',vf.views.test2.id
        #         )
        # mf.explores.test1.test2.setRelationship('many_to_one')
        # mf.explores.test1.test2.setType('left_outer')
        #TODO: check assigning a whole list to a type
        # test1.foo.suggestions = ['suggestion1']
        #### End Modifications ###
        with open('lookml/tests/kitchenSink/kitchenSink2.model.lkml', 'w') as f:
            f.write(self.f_copy.__str__())

    # @unittest.expectedFailure
    def test_step6(self):
        '''
            6) Fetch and parse KitchenSink2 and test the successful addition of attributes in step 5
        '''
        self.f2 = lookml.File('lookml/tests/kitchenSink/kitchenSink2.model.lkml')
        order_items2 = self.f2.views.order_items
        #Check Sql Change
        self.assertEqual(order_items2.id.sql.value,"${TABLE}.test_sql_change")
        #Check dimension Addition:
        self.assertIsInstance(order_items2.test_add_dimension, lookml.Dimension)

        #Check view is still the same length + 1 (added one field in the prior test case)
        self.assertEqual(len(order_items2),48)

        #Check searching dimensions by sql:
        self.assertEqual(1,len(list(order_items2.search('sql','\$\{shipped_raw\}'))))

        #Check renamed field has the correct number of direct children
        self.assertEqual(1, len(list(order_items2.time_in_transit.children())))

        # print(*[str(f) for f in order_items2.dims()])
        # print(order_items2.stringify(order_items2.dims_sorted()))
        
        # print(
        #     lookml.stringify(
        #         lookml.sortMe(order_items2.dims())
        #     )
        # )

        # for dim in order_items2.dims_sorted():
        #     print(dim)



    def tearDown(self):
        '''
            remove KitchenSink2 if it exists (comment teardown out if having step6 difficulties and need to inspect kitchensink2)
        '''
        pass
        

    def test_github_loop(self):
        proj = lookml.Project(
                 repo= config['github']['repo']
                ,access_token=config['github']['access_token']
                ,looker_host="https://profservices.dev.looker.com/"
                ,looker_project_name="russ_sanbox"
        )
        vf = proj.file('simple/tests.view.lkml')
        mf = proj.file('simple/test1.model.lkml')
        
        proj.update(vf)
        proj.update(mf)
        # proj.deleteFile('great_test2.view.lkml')
        myNewView = lookml.View('great_test2') + 'id' + 'count_of_total' + 'worked' + 'poop'
        myNewView.id.sql = "${TABLE}.`id`"
        myNewView.id.setType('string')
        myNewFile = lookml.File(myNewView)
        proj.put(myNewFile)
        proj.deploy()
        # print(myNewFile.path)
        # print(myNewFile)
        # proj.add(myNewFile)
        # print(proj.exists('nope.txt'))
        # print(proj.exists('simple/tests.view.lkml'))


if __name__ == '__main__':
    unittest.main()