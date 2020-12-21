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
        #test to ensure that primary key is added, then if another primary key is set it throws an error, unless
        #the original primary key was set to no prior to the operation
        lookml.OMIT_DEFAULTS = True
        x = lookml.View('''
                view: x {
                    dimension: x {
                        primary_key: yes
                    }
                    dimension: y {}
                }
            ''')
        with self.assertRaises(lang.DuplicatePrimaryKey) as context:
            x.y.primary_key = 'yes'
        x.x.primary_key = 'no'
        # print(x)
        x.y.primary_key = 'yes'
        #P2: document that this is the way to print and __pk does not return the pk
        # print(x)
        # print(x._View__pk)
    
    def test_coexistance_error(self):
        #checks to ensure the add_hook / exception process is working
        x = lookml.View('foo')
        x.sql_table_name = 'public.foo'
        with self.assertRaises(lang.CoexistanceError) as context:
            x + 'derived_table: { sql: select * from foo ;; }'
        del x.sql_table_name
        x + 'derived_table: { sql: select * from foo ;; }'
        with self.assertRaises(lang.CoexistanceError) as context:
            x.sql_table_name = 'public.foo'





class testView(unittest.TestCase):
    '''
        Read a view file, test its methods and manipulation
    '''
    def setUp(self):
        pass

    def test_parse_print(self):
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])
        print(self.myView)

    def test_filters(self):
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])
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
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])
        self.assertIsNotNone(self.myView._json())
        print(self.myView._json())

    def test_refs(self):
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])
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

    def test_addition(self):
        tmp = lookml.View('''
            view: foo {
                derived_table: {
                    explore_source: order_items {
                        column: id { field: id }
                        column: id_2 { field: id }
                    }
                }
            }
        ''')
        tmp.derived_table.explore_source.column + 'column: foo {}'
        tmp.derived_table.explore_source + 'limit: 500'
        self.assertTrue('column: id_2 ' in str(tmp.derived_table.explore_source))
        print(tmp)



    def test_tags(self):
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])
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
                        datagroup_trigger: foo
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
        cool = ['test123','test456','test890']
        x.explores['trip'] + ''.join([f'''
         join: {item} {{}}
         ''' for item in cool])
        self.assertTrue('test890' in str(x.explores.trip))

    def test_other(self):
        self.parsed_view = lkml.load(open('tests/files/basic_parsing/basic.view.lkml'))
        self.myView = lookml.View(self.parsed_view['views'][0])
        # if isinstance(self.myView.sum_foo.sql,lookml.prop):
        # if not isinstance(self.myView.sum_foo.sql,tuple()):
        # if (True if self.myView.sum_foo.sql._type() == '' else False):
        #     print('wow')
        # pprint(self.myView.transaction.__dict__)
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
        # self.myView.set.set1.fields + 'foo'
        print(self.myView.foo.link[0].url.value)
        # print(self.myView)
        # for p in self.myView.bar.__iter__(type=lookml.prop):
        # for p in self.myView.transaction(type=lookml.prop, sub_type='timeframes', exclude_subtype='timeframes'):
        #     # if isinstance(p,lookml.prop_list_unquoted):
        #     print(p)
    def test_plural_anonymous_constructs(self):
        raw = '''
        view: x {
            derived_table: {
                explore_source: order_items {
                    column: id { field: order_items.id }
                    column: date { field: order_items.created_date }
                    column: status { field: order_items.status }
                    bind_filters: {
                        from_field: created_date
                        to_field: date
                    }
                    bind_filters: {
                        from_field: order_items.id
                        to_field: id
                    }
                    bind_filters: {
                        from_field: order_items.status
                        to_field: status
                    }
                }
            }
                dimension: date { type: date }
                dimension: id { type: number }
                dimension: status { 
                    type: string 
                    link: {
                        url: "http://facebook.com"
                    }
                    link: {
                        url: "http://yahoo.com"
                    }
                    link: {
                        url: "http://myspace.com"
                    }
                    }
                measure: count { type: count }
        }
        '''
        x = lookml.View(raw)
        self.assertTrue(x.derived_table.explore_source.bind_filters[0].from_field.value=='created_date')
        i = 0
        for item in x.derived_table.explore_source.bind_filters:
            i +=1 
        self.assertEqual(i,3)
        x.status.link + 'link: { url: "http://foo.com" }'
        # print(x.status.link)
        
        self.assertTrue(x.status.link[3].url.value=='http://foo.com')
        x.status.link[3].remove()
        i=0
        for link in x.status.link:
            i += 1
        self.assertEqual(i,3)

    #P0: add support for getitem[] syntax at all levels
    def test_all_subscriptability(self):
        pass
        #test file from project
        #test view/explore/prop from file/model
        #test field/prop from view
        #test prop from field
        

    def test_constructor(self):
        a = lookml.View('''
            view: foo {
                sql_table_name: public.order_items ;;
                dimension: foo {}
                measure: count {}
            }
        ''')
        self.assertTrue(isinstance(a,lookml.View))
        self.assertEqual(a.name,'foo')
        b = lookml.View('foo')
        self.assertTrue(isinstance(b,lookml.View))
        self.assertEqual(b.name,'foo')
        c = lookml.View({'name':'foo'})
        self.assertTrue(isinstance(c,lookml.View))
        self.assertEqual(c.name,'foo')
        with self.assertRaises(Exception) as context:
            lookml.View('''
            view: foo {
                sql_table_name: public.order_items ;;
                dimension: foo {}
                measure: count {}
            }
            view: bar {}
            ''')
        self.assertTrue('contains more than one view' in str(context.exception))
        #P3 does not throw the right exception, something is wrong with the ws.view_pattern and checker function
        with self.assertRaises(Exception) as context:
            lookml.View('explore: foo {}')
        # self.assertTrue('contains more than one view' in str(context.exception))
        
    def test_sql_enahancement_methods(self):
        tmp = lookml.View(
            '''
            view: tmp {
                dimension: foo {
                    sql: ${TABLE}.foo ;;
                }
            }
            '''
        )
        #P3: add arguments and date casting 
        tmp.foo.sql.nvl()
        self.assertTrue('nvl' in tmp.foo.sql.value)
        print(tmp)

    def test_more_add_hooks(self):
        #P2: other rules that should be run: various coexistence errors
        #P3: run coexistence errors and warnings and put to CSV
        foo = lookml.View('view: foo {}')
        foo + 'dimension: foo {}'
        # throws an assertion error:
        # foo.foo + 'type: count'


    def test_legacy_methods(self):
    #     #P0: legacy / backward compatibility methods: 
    #     #addProperty, addDimension, addMeasure, addJoin etc....
        x = lookml.View('x')
        #P0: add multi-constructor capabilities to all LookML objects
        # foo = lookml.Dimension('foo')
    #     x.addField(foo)
    #     x.getPrimaryKey()
    #     x.removeField(foo)
    #     x.addField(foo)
    #     x.search('sql','${TABLE}')
    #     x.setExtensionRequired()
    #     x.setPrimaryKey(x.foo)
    #     for i in x.fieldNames():
    #         print(i)
    #     for i in x.fields():
    #         print(i)
    #     #P3 dimensions()
    #     # for i in x.dimensions():
    #     #     print(i)
    #     for i in x.dimensionGroups():
    #         print(i)
    #     for i in x.filters():
    #         print(i)
    #     for i in x.getFieldsByTag('my_tag'):
    #         print(i)
    #     for i in x.getFieldsByTag('my_tag'):
    #         print(i)
    #     for i in x.getFieldsByType('string'):
    #         print(i)
    #     for i in x.getFieldsSorted():
    #         print(i)
    #     foo.setProperty('sql','${TABLE}.foo')
    #     foo.setMessage('comment')
    #     foo.getMessage()
    #     foo.addTag('my_tag')
    #     foo.setName('foo1')
    #     foo.setPrimaryKey()
    #     bar = lookml.Dimension('bar')
    #     x.addDimension(bar)
    #     bar.setType('number')
    #     x.addCount()
    #     # x.addAverage(x.foo)
    #     # x.addComparisonPeriod(x.foo,'')
    #     x.addCountDistinct(x.foo)
    #     x.sum(x.foo)
    #     x.sumAllNumDimensions()
    #     bar.setView(x)
    #     bar.setViewLabel("foo")
    #     # foo.setName_safe('wawa')
    #     # x.unSetPrimaryKey()
    #     bar.hasProp('view_label')
    #     bar.rawProp('view_label')
    #     foo.setDescription('this is very cool')
    #     foo.setAllLabels( group: None, item: None, label: None)
    #     foo.setDBColumn( dbColumn, changeIdentifier=True)
    #     foo.setTier(tiers=[])
    #     foo.setSql('')
    #     foo.setType('')
    #     foo.setNumber()
    #     foo.setString()
    #     foo.removeTag()
    #     foo.addLink(url,label,icon_url='https://looker.com/favicon.ico')
    #     for i in foo.children():
    #         print(i)



    def test_new_file(self):
        pass

#P2: obtain the real list of timezones from Looker itself
#P3: add CLI support
#P3: option to omit defaults
#P3: add looker version numbers to the lang map and throw warning if prop depreicated or error if not yet supported

class testOtherFiles(unittest.TestCase):
    def setUp(self):
        pass

    def test_parsing_aggregate_tables(self):
        #P0: include coming back funny becuase it's the wrong type. Needs to be multi-value / list type, but print as string
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