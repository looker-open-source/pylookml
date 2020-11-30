import lookml, lang
import unittest
import lkml as lkml
from pprint import pprint
import file, project
import warnings
import configparser
config = configparser.ConfigParser()
config.read('tests/settings.ini')

# Objective / coverage
#     Read all file types from filesystem: 
#     model, 
#     view, 
#     other lkml files, 
#     manifest, 
#     dashboard, 
#     js, 
#     json, 
#     maplayer
#     Read Files with isolated types of special syntax:
#     filters: old and new syntax
#     materializations
#     extensions
#     refinements

class testExceptions(unittest.TestCase):
    def setup(self): pass
    def test_invalid_lookml_attribute(self):
        with self.assertWarns(UserWarning) as wrn:
            testView = lookml.View({})
            testView.name = 'test'
            testView + '''
                dimension: foo {
                    cray: "cha"
                }
            '''
            # Verify
            for w in wrn.warnings:
                print(w)

    def test_duplicate_primary_key(self):
        #P0: test to ensure that primary key is added, then if another primary key is set it throws an error, unless
        #the original primary key was set to no prior to the operation
        pass

class testView(unittest.TestCase):
    '''
        Read a view file, test its methods and manipulation
    '''
    def setUp(self):
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])

    def test_parse_print(self):
        print(self.myView)

    def test_filters(self):
        self.myView.sum_foo.filters.foo.contains('test')
        self.myView + '''
            measure: total_sales {type: sum sql: ${TABLE}.sales ;;}
        '''
        self.myView.total_sales + 'filters: [foo:">100"]'
        self.myView.total_sales.filters + {'bar':'>100'}
        self.assertEqual(self.myView.total_sales.filters.bar.value,'>100')
        self.assertEqual(self.myView.total_sales.filters.foo.value,'>100')
        self.assertEqual(self.myView.sum_foo.filters.foo.value,'%test%')

    def test_json_serialization(self):
        self.assertIsNotNone(self.myView._json())
        print(self.myView._json())

    def test_refs(self):
        for f in self.myView._fields():
            #full reference
            print('full ref __ref__: ',f.__ref__)
            #short reference
            print('short ref __refs__: ',f.__refs__)
            #full reference -- regex escaped
            print('full ref regex __refre__: ',f.__refre__)
            #Short reference -- regex escaped
            print('short ref regex __refsre__: ',f.__refsre__)
            #Raw Reference
            print('raw full ref __refr__: ',f.__refr__)
            #Raw refence short
            print('raw ref short __refrs__: ',f.__refrs__)
            #Raw Reference regex
            print('raw ref regex __refrre__: ',f.__refrre__)


    def test_tags(self):
        self.myView.transaction.tags + ['tag5','tag6','tag7','tag8']
        self.myView.transaction.tags - 'tag7'
        self.myView.transaction.tags - ['tag6','tag4']
        self.assertTrue('tag3' in self.myView.transaction.tags)
        for tag in self.myView.transaction.tags:
            if tag == 'tag8':
                self.myView.transaction.tags - tag
        self.assertCountEqual(self.myView.transaction.tags,['tag1','tag2','tag3','tag5'])

    def test_delete_me_adhoc_model_test(self):
        x = '''
            connection: "my_data"
            view: foo {
                dimension: a {
                    type: string
                    primary_key: yes
                }
                dimension: b {
                    #primary_key: yes
                }
                dimension: c {}
            }
            view: bar {
                dimension: x {}
                dimension: y {}
                dimension: z {}
            }
            explore: bar {
                join: foo {}
                join: test12 {}
            }
            explore: foo {
                join: bar {}
                aggregate_table: blah {
                    query: {
                        dimensions: [dim1,dim2,dim3]
                        filters: [foo:"%myfoo%",bar:"mybar%"]
                        sorts: [dim1: asc]
                        pivots: [dim4]
                    }
                    materialization: {
                        datagroup_trigger: yes
                    }
                }
            }
        '''
        parsed = lkml.load(x)
        # print(parsed)
        m = lookml.Model(parsed)
        # print(str(m.__dict__))
        
        m.views.foo.a.primary_key.value = 'no'
        m.views.foo.b.primary_key = 'yes'
        print(str(m))
        # print(str(m.explores['foo']))
        # print(str(m.explores.foo))

    def test_deleteme_adhoc_file_model_binding(self):
        x = file.File('tests/files/basic_parsing/basic.model.lkml')
        print(x.path)
        cool = 'test123'
        #P0: replacing rather than additive
        x.explores['trip'] + f'''
        join: {cool} {{

        }}
        '''
        x.path = 'example2.model.lkml'
        x.write()

    def test_other(self):
        # if isinstance(self.myView.sum_foo.sql,lookml.prop):
        # if not isinstance(self.myView.sum_foo.sql,tuple()):
        # if (True if self.myView.sum_foo.sql._type() == '' else False):
        #     print('wow')
        # pprint(self.myView.transaction.__dict__)
        #P0: fix link accessors
        # print(self.myView.foo.link[0])
        # if 'transaction' in self.myView:
        #     print(self.myView.transaction)
        #P0: list size changed during iteration unless call parentheses are added
        # for i in self.myView.bar():
        #     print(i)
        # if self.myView.suggestions:
        #     print('<<your yesno is True>>')
        # else:
        #     print('<<your yesno is False>>')
        # print(type(self.myView.transaction.tags))
        # print(lang.props._allowed_children['dimension_group'])
        # print(self.myView.derived_table.sql.value)
        # for f in self.myView(type=lookml.Field):
        #     if f.type.value == 'string':
        #         self.myView + f'measure: sum_{f.name} {{ type: sum sql: {f.__refs__};; }}'
        # print(lang.props._allowed_children['dimension'])
        # self.myView.sum_foo.direction = 'row'
        # for field in self.myView(type=lookml.Field):
        #     if '${TABLE}' in field.sql:
        #         print(field.name,": ", field.sql)
        # for f in self.myView._first_order_fields():
        #     print(f.sql)
        # print(self.myView.__dict__)
        # print(self.myView.set.__dict__)
        # print(self.myView.set.set1)
        self.myView.set.set1.fields + 'foo'
        print(self.myView.foo.link[1])
        # for p in self.myView.bar.__iter__(type=lookml.prop):
        # for p in self.myView.transaction(type=lookml.prop, sub_type='timeframes', exclude_subtype='timeframes'):
        #     # if isinstance(p,lookml.prop_list_unquoted):
        #     print(p)
class testOtherFiles(unittest.TestCase):
    def setUp(self):
        pass

    def test_parsing_aggregate_tables(self):
        #P0: include coming back funny
        x = file.File('tests/files/basic_parsing/agg.model.lkml')
        # x = lkml.load(open('tests/files/basic_parsing/agg.model.lkml','r', encoding="utf-8"))
        # x = open('tests/files/basic_parsing/agg.model.lkml','r', encoding="utf-8")
        print(str(x))
        print(x.explores.foo.aggregate_table.bar)

    def test_model_file(self):
        self.model_file = file.File('tests/files/basic_parsing/basic.model.lkml')
        print(str(self.model_file))

    def test_view_refinement(self):
        x = file.File('tests/files/basic_parsing/refine.view.lkml')
        print(str(x))

    def test_other_lkml_file(self):
        pass

    def test_manifest_file(self):
        #P0: accessors and namespace for manifest file is bunk
        x = file.File('tests/files/basic_parsing/manifest.lkml')
        #anon: local_dependency, visualization, 
        #named: constant, application, 
        #other props / project name etc 
        
        print(str(x.contents.project_name))

    def test_project_connectivity(self):
        proj = project.Project(
            repo= "llooker/russ_sandbox",
            access_token=config['project1']['access_token'],
        )

        # mf = proj.file('01_order_items.view.lkml')
        for f in proj.files():
            print(f.path)
            for v in f.contents.views.values():
                print(' '*2,v.name)
        #P0: iterate over: f.views:, f.views['order_items'], f.views.order_items
        #P0: create a new type of each file
        #P0: context manager for project

        # mf = proj.file('11_order_facts.view.lkml')
        # print(str(mf))

    def test_dashboard_file(self):
        pass
    def test_js_file(self):
        pass
    def test_json_file(self):
        pass
    def test_maplayer_topojson(self):
        pass

    # def tearDown(self):
    #     pass