import lookml.lookml as lookml
import unittest
import lkml as lkml
from pprint import pprint

class test_things(unittest.TestCase):
    def setUp(self):
        self.parsed = lkml.load(open('tests/files/basic_test.view.lkml'))

    def test_1(self):
        x = lookml.View(self.parsed['views'][0])
        x.sum_bar.filters.foo.contains('mexico')
        x.sum_bar.filters.baz = ''
        x.sum_bar.filters.baz.contains('foo')
        x.foo.type = 'number'
        print(x.foo._data)
        print(str(x))

    def test_set(self):
        x = lookml.View(self.parsed['views'][0])
        x.bar.name = 'wawa'
        # x.transaction.tags.value.append('hello,world!')
        # x.transaction.tags.value = ['foo','bar']
        
        x.sum_foo.filters.whoop = 'changed'
        print(x.sum_foo.filters.foo.value)
        print(x.sum_foo.filters._data)
        print(x.sum_bar.filters._data)
        # print(x.sum_foo.filters.foo._data)
        print(x.sum_foo.filters)

    def test_json(self):
        v = lookml.View(self.parsed['views'][0])
        pprint(v.sum_bar.json())

    def test_lookml_dashboard(self):
        dash = lookml.LookMLDashboard('tests/files/test.dashboard.lookml')
        pprint(dash.json())

    def test_addition(self):
        v = lookml.View(self.parsed['views'][0])
        v + '''
            dimension: my_addition { }
            '''
        v.sum_bar + '''
            type: count
        '''
        v.addDimension('successful_test_addition')
        print(v)

    def test_string_field_addition(self):
        order_items = lookml.View('order_items')
        order_items.sql_table_name = 'public.foo'
        order_items.addDimension('my_added_dimension')
        order_items.addMeasure('my_added_measure')
        order_items.addFilter('my_added_filter')
        order_items.addParameter('my_added_parameter')
        pprint(order_items._fields)
        print(order_items)

    def test_ndt(self):
        parsed = lkml.load(open('tests/files/test_ndt.view.lkml'))['views'][0]
        # pprint(parsed)
        x = lookml.View(parsed)
        print(x.derived_table.explore_source._columns['country'].field)
        #P0: add . accessors for columns
        #P0: add support for bind filters and other explore source properties
        # print(x._props['derived_table']._props['explore_source']._props)
        # print(x._props['derived_table']._props['explore_source']._columns)
        # print(x)

    def test_list_prop_iteration(self):
        v = lookml.View(self.parsed['views'][0])
        v.foo.tags = ['t1','t2','t3']
        for t in v.transaction.timeframes:
            print(t)
        print(v.foo)

    def test_view_field_iteration(self):
        v = lookml.View(self.parsed['views'][0])
        for f in v:
            f.addProp('tags',['wow'])
            print(f.__ref__,': ',f)
        print(v)

    def test_field_ref(self):
        v = lookml.View(self.parsed['views'][0])
        print('ref __ref__: ',v.foo.__ref__)
        print('ref short __refs__: ',v.foo.__refs__)
        print('ref regex __refre__: ',v.foo.__refre__)
        print('ref short regex __refsre__: ',v.foo.__refsre__)
        print('ref raw __refr__: ',v.foo.__refr__)
        print('ref raw short __refrs__: ',v.foo.__refrs__)
        print('ref raw regex __refrre__: ',v.foo.__refrre__)
