import unittest
import lookml,lkml

class testField(unittest.TestCase):
    def setUp(self):
        self.order_items = lookml.View('order_items')
        self.order_items + 'inventory_item_id' + 'id' 
        lookml.config.PRE_FIELD_BUFFER = ''
        lookml.config.POST_FIELD_BUFFER = ''

    # def test_print(self):
    #     print(self.order_items)


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

    def test_calling_non_existent_field(self):
        with self.assertRaises(KeyError):
            self.view.getField('fake_field')
            
    def test_false_addition(self):
        # Check that the view complains if incorrect object is added
        with self.assertRaises(Exception):
            explore = lookml.Explore('order_items')
            self.view + explore

    def test_extension(self):
        extended_view = self.view.extend(sameFile=False,required=True)
        self.assertIsInstance(extended_view,lookml.View)
        self.view + 'id'
        # print(self.view)
        # self.view.write()
        
        extended_view + 'id'
        extended_view.id.hide()
        # print(extended_view)
        # extended_view.write()

# class testExplore(unittest.TestCase):
#     def setUp(self):
#         self.order_items = lookml.View('order_items')
#         self.order_items + 'inventory_item_id' + 'id' 
#         self.inventory_items = lookml.View('inventory_items')
#         self.inventory_items + 'id' + 'product_id'
#         self.products = lookml.View('products')
#         self.products + 'id' + 'name'
#         self.order_items_explore = lookml.Explore(self.order_items)

#     def test_existance(self):
#         self.assertTrue(isinstance(self.order_items_explore,lookml.Explore))

#     def test_addition_of_joins(self):
#         '''' tests the addition of joins '''
#         self.order_items_explore.addJoin(self.inventory_items).on(self.order_items.inventory_item_id , ' = ', self.inventory_items.id).setType('left_outer').setRelationship('one_to_one')
#         self.order_items_explore.addJoin(self.products).on(self.inventory_items.product_id , ' = ', self.products.id).setType('left_outer').setRelationship('many_to_one')
#         self.assertEqual(len(self.order_items_explore),2)
#         #print(self.order_items_explore)

#     def test_create_ndt(self):
#         pass


class testParserBinding(unittest.TestCase):
    def setUp(self):
        # import os
        # cwd = os.getcwd()
        # print(cwd)
        with open('lookml/tests/thelook/order_items.view.lkml', 'r') as file:
            self.parsed = lkml.load(file)

    def test_print_file(self):
        if 'views' in self.parsed.keys():
        # f = list()
            for view in self.parsed['views']:
                tmpView = lookml.View(view)
                pass




if __name__ == '__main__':
    unittest.main()





# order_items = lookml.View('order_items').setSqlTableName(sql_table_name='public.order_items')
# order_items + 'id' + 'value' + 'inventory_item_id'
# order_items.id.setNumber()
# order_items.inventory_item_id.setNumber()
# order_items.addSum('value')
# order_items + lookml.DimensionGroup('created_at') 

# products = lookml.View('products')
# products + 'id' + 'name'

# inventory_items = lookml.View('inventory_items').setSqlTableName(sql_table_name='public.inventory_items')
# inventory_items + 'id' + 'product_id'


# order_items_explore = lookml.Explore(order_items)
# order_items_explore.addJoin(inventory_items).on(order_items.inventory_item_id , ' = ', inventory_items.id).setType('left_outer').setRelationship('one_to_one')
# order_items_explore.addJoin(products).on(inventory_items.product_id , ' = ', products.id).setType('left_outer').setRelationship('many_to_one')



# the_look = lookml.Model('the_look')
# the_look.setConnection('my_connection')
# the_look.include(order_items)
# the_look.include(inventory_items)
# the_look.addExplore(order_items_explore)


# the_look.order_items.order_items.id.addLink(
#     url='/dashboards/7?brand=cool',
#     label=''
# )

# product_facts_ndt = order_items_explore.createNDT(explore_source=order_items_explore, name='product_facts_ndt',fields=[products.id,order_items.total_value])
# product_facts_ndt.addSum('total_value')
# the_look.include(product_facts_ndt)
# product_facts_ndt.write()
# order_items_explore.addJoin(product_facts_ndt).on(products.id,' = ',product_facts_ndt.id).setType('left_outer').setRelationship('one_to_one')

# the_look.write()
# order_items.write()
# products.write()
# inventory_items.write()
