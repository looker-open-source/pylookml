import unittest
import lookml,lkml

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




    # def test_existance(self):
    #     self.assertTrue(isinstance(self.order_items_explore,lookml.Explore))
    #     # self.assertTrue(isinstance(self.parsedExplore,lookml.Explore))

    # def test_addition_of_joins(self):
    #     '''' tests the addition of joins '''
    #     self.order_items_explore.addJoin(self.inventory_items).on(self.order_items.inventory_item_id , ' = ', self.inventory_items.id).setType('left_outer').setRelationship('one_to_one')
    #     self.order_items_explore.addJoin(self.products).on(self.inventory_items.product_id , ' = ', self.products.id).setType('left_outer').setRelationship('many_to_one')
    #     self.assertEqual(len(self.order_items_explore),2)

    # def test_create_ndt(self):
    #     pass


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
        file3.write(str(v2))
        file3.close()
        

    def test_model_loop(self):
        file1 = open('lookml/tests/thelook/thelook_test.model.lkml', 'r')
        lkmljson = lkml.load(file1)
        
        if 'explores' in self.parsed.keys():
            for explore in self.parsed['explores']:
                self.parsedExplore = lookml.Explore(explore)
                x = lookml.Join({
                        'name': 'order_facts', 
                        'relationship': 'many_to_one', 
                        'sql_on': 'foo', 
                        'type': 'left_outer', 
                        'view_label': 'Orders'
                        })
                pass
        file3 = open('lookml/tests/thelook/test.out2.lkml', 'w')
        
        v = None
        for explore in self.parsed['explores']:
            self.parsedExplore = lookml.Explore(explore)


        file2 = open('lookml/tests/thelook/test.out.lkml', 'w')
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
        file3.write(str(v2))
        file3.close()

        with open('lookml/tests/thelook/thelook_test.model.lkml', 'r') as file:
            self.parsed = lkml.load(file)
            pass
    


    # def test_dispatch(self):
        # pass
        '''
        1) Grab an arbirary file and create an index of all the stuff inside
        2) Ensure that there is a namespacing mechanism from the "file" point of view
        ? File Class?
        ? This might make sense in anothr test case....
        '''

if __name__ == '__main__':
    unittest.main()