import unittest
import lookml,lkml
import configparser
config = configparser.ConfigParser()
config.read('lookml/lookml/config/settings.ini')
class testField(unittest.TestCase):
    def setUp(self):
        self.order_items = lookml.View('order_items')
        self.order_items + 'inventory_item_id' + 'id' 
        lookml.config.PRE_FIELD_BUFFER = ''
        lookml.config.POST_FIELD_BUFFER = ''

class testView(unittest.TestCase):
    def setUp(self):
        self.view = lookml.View('order_items')

    def test_field_addition(self):
        self.view + 'id'
        field2 = lookml.Dimension('cool')

        self.view + field2
        self.view.cool.setType('number')

        self.assertEqual(len(self.view),2)
        self.assertEqual(self.view.id.type.value,'string')
        self.assertEqual(self.view.cool.type.value,'number')

    def test_correct_type(self):
        self.assertTrue(isinstance(self.view,lookml.View))
    
    def test_correct_name(self):
        self.assertEqual(self.view.name,'order_items')

    def test_extension(self):
        extended_view = self.view.extend(sameFile=False,required=True)
        self.assertIsInstance(extended_view,lookml.View)
        self.view + 'id'        
        extended_view + 'id'
        extended_view.id.hide()


class testParserBinding(unittest.TestCase):
    def setUp(self):
        with open('lookml/tests/thelook/test.lkml', 'r') as file:
            self.parsed = lkml.load(file)
            pass
        if 'views' in self.parsed.keys():
            for view in self.parsed['views']:
                self.tmpView = lookml.View(view)

    def test_view_loop(self):
        file1 = open('lookml/tests/thelook/test.lkml', 'r')
        file2 = open('lookml/tests/thelook/test.out.lkml', 'w')
        file3 = open('lookml/tests/thelook/test.out2.lkml', 'w')
        lkmljson = lkml.load(file1)
        file1.close()
        v = None
        if 'views' in lkmljson.keys():
                for view in lkmljson['views']:
                    v = lookml.View(view)
        v + 'id'
        v + 'bar'
        v.id.sql = "COALESCE(${TABLE}.id,0)"
        v.id.addTag('Generated Code')
        v.foo.sql = "COALESCE(${TABLE}.id,0)"
        v.foo.addTag('Generated Code')
        v.bar.setMessage('this is bar')
        v.id.setMessage('Auto Generated -- Dont touch')
        file2.write(v.__str__())
        file2.close()
        file2 = open('lookml/tests/thelook/test.out.lkml', 'r')
        v2 = None
        lkmljson2 = lkml.load(file2)
        if 'views' in lkmljson2.keys():
                for view in lkmljson2['views']:
                    v2 = lookml.View(view)
        v2 - 'id'
        v2.tst.addTag('foo')
        v2 + lookml.Measure('count_of_total')
        v2.count_of_total.setType('sum')
        v2.count_of_total.sql = '${id}'
        file2.close()
        file3.write(str(v2))
        file3.close()
        

    def test_model_loop(self):
        file1 = open('lookml/tests/thelook/thelook_test.model.lkml', 'r')
        lkmljson = lkml.load(file1)
        file1.close()
        if 'explores' in lkmljson.keys():
            for explore in lkmljson['explores']:
                self.parsedExplore = lookml.Explore(explore)

        file2 = open('lookml/tests/thelook/thelook_test2.model.lkml', 'w')
        ###### MANIPULATE ######
        # print(self.parsedExplore.order_facts.relationship)
        self.parsedExplore.order_facts.setOn('FOO')
        ###### MANIPULATE ######
        file2.write(str(self.parsedExplore))
        file2.close()
        file2 = open('lookml/tests/thelook/thelook_test2.model.lkml', 'r')
        lkmljson = lkml.load(file2)
        if 'explores' in lkmljson.keys():
            for explore in lkmljson['explores']:
                self.parsedExplore = lookml.Explore(explore)
        file2.close()
        file3 = open('lookml/tests/thelook/thelook_test3.model.lkml', 'w')
        file3.write(str(self.parsedExplore))
        file3.close()


    def test_github_loop(self):
        proj = lookml.Project(
                repo= config['github']['repo'],
                access_token=config['github']['access_token']
        )
        vf = proj.getFile('simple/tests.view.lkml')
        mf = proj.getFile('simple/test1.model.lkml')
        
        #loop over views
        for y in vf.views:
            pass

        #Look up view objects from a file and give them a convenient name:
        test1 = vf.views.test1
        test2 = vf.views.test2

        #look up an explore
        mf.explores.test1.test2.on(
                vf.views.test1.foo,'=',vf.views.test2.id
                )
        mf.explores.test1.test2.setRelationship('many_to_one')
        mf.explores.test1.test2.setType('left_outer')

        #Manipulate field sql
        test1.foo.sql = "${TABLE}.foo"
        test1.foo.sql_nvl("0")
        
        #Tags, suggestions and ephemeral comments
        test1.foo.addTag("Generated Code")
        test1.foo.tags + 'tag_xyz'
        test1.foo.removeTag("tag_xyz")
        # loop over tags
        for tag in test1.foo.tags:
            pass
            #print(tag)
        test1.foo.setMessage("Auto Generated Code... comments in this will file may disappear on automation run")
        test1.foo.suggestions = ['suggestion1']
        if 'Generated Code' in test1.foo.tags:
            test1.foo.tags + 'Detected Generated Code'
        if 'suggestion' in test1.foo.suggestions:
            test1.foo.suggestions + 'suggestion2'
        
        test1.sumAllNumDimensions()

        for field in test1.getFieldsByType('sum'):
            field.tags + 'sum'


        test1 + lookml.DimensionGroup('created')

        test1.addComparisonPeriod(test1.foo,test1.created)

        #Obtain lookml fields by tag
        for f in test2.getFieldsByTag('x'):
            #do work
            f.removeTag('x')
        
        #Add a new view
        newView = lookml.View('test3')
        newView + 'id'
        newView.id.type = 'number'
        newView.id.sql = "${TABLE}._id_"
        vf + newView

        test1.extend()
        # chris =  lookml.ndt(mf.explores.test1).addColumn('chris',test1.foo)
        # print(chris)
        proj.updateFile(vf)
        proj.updateFile(mf)
        # proj.newFile(lookml.File(lookml.View('test4')))




#TODO: Add test coverage for providing positional arguments of vastly different types, i.e. lookml class vs json etc. 



if __name__ == '__main__':
    unittest.main()