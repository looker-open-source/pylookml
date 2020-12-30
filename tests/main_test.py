import lookml, lang
import unittest, copy, json
import lkml as lkml
from pprint import pprint
import file, project
import warnings
import configparser
config = configparser.ConfigParser()
import pprint
# config.read('tests/settings.ini')
config.read('settings.ini')
#P3: query can exist under the explore or aggregate table
#P2: subtraction hooks / warnings
#P3: put colin's recursive sql table finder in the library
#P2: test coverage for sets
#P3: test coverage for manifest files
#P2: organize the tests

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

class testMain(unittest.TestCase):
    '''
        Read a view file, test its methods and manipulation
    '''
    def setUp(self):
        pass

    def test_model_file(self):
        pm = lkml.load(open('.tmp/pylookml/eav_example/eav.model.lkml'))
        p = lookml.Model(pm)
        print(p)


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

    def test_adhoc_model_test(self):
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

    def test_file_model_binding(self):
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
        #P1: list size changed during iteration unless call parentheses are added
        # for i in self.myView.bar():
        #     print(i)
        self.assertTrue(self.myView.suggestions)
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

    def test_anonymous_construct(self):
        #P1 support addition like lookml objects / pull out common addition functions
        # add, insert, add_hook, sub, subhook etc
        pass
    #P0: add support for getitem[] syntax at all levels
    def test_all_subscriptability(self):
        proj = project.Project(**config['project1'])
        # print(proj['order_items.view.lkml']['views']['order_items']['id'].primary_key.value)
        print(proj['order_items.view.lkml']['views']) 
        
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
        x = lookml.Dimension('foo')
        y = lookml.Measure('bar')
        z = lookml.Filter('baz')
        aa = lookml.Parameter('fizz')
        ab = lookml.Dimension_Group('buzz')
        print(x,y,z,aa,ab)
        x = lookml.Dimension('dimension: foo { type: string }')
        y = lookml.Measure('measure: bar{ type: count }')
        z = lookml.Filter('filter: baz { type: date }')
        aa = lookml.Parameter('parameter: fizz { type: unquoted }')
        ab = lookml.Dimension_Group('dimension_group: buzz { type: time }')
        print(x,y,z,aa,ab)
        exp = lookml.Explore('my_explore')
        # jn = lookml.Join('my_join')
        # mdl = lookml.Model('my_model')
        # mnfst = lookml.Manifest('my_manifest')
        # print(exp,jn,mdl,mnfst)
        print(exp)
        exp1 = lookml.Explore('''explore: my_explore {
            join: foo {}
        }''')
        print(exp1)
        # mdl1 = lookml.Model('conection: "cool" ')
        # mnfst1 = lookml.Manifest('project_name: "example"')
        # print(exp1,jn1,mdl1,mnfst1)
        # print(exp1,jn1)

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
    def test_adding_joins_to_explore(self):
        #P0 
        pass
    def test_adding_fields_to_view(self):
        #P0
        pass

    def test_set_property(self):
        x = lookml.Dimension('''
        dimension: x {}
        ''')
        x.setProperty('sql','${TABLE}.foo')
        self.assertEqual(x.sql.value,'${TABLE}.foo')
        y = lookml.View('y')
        y.setProperty('sql_table_name', 'public.order_items')
        self.assertEqual(y.sql_table_name.value,'public.order_items')

    def test_children_ancestors(self):
        # field.children() -> direct chilren
        #field.children_all() -> all chilren multi generation
        #field.dependency_chain(view=self.parent) -> tuple chain
        #view.print_dependency_map(format='human' or 'csv') -> print out of dep chains in view
        #field.print_dependency_map() -> print out of dep chain at field level
        #field.ancestors() -> any directs in the field
        #field.ancestors_all() -> any fields referenced up to ${TABLE}
        #field.print_ancestor_map() -> prints all fields which are on ancestor chain
        v = lookml.View('''
            view: v {
                dimension: a {}
                dimension: c { sql: ${a} ;; }
                dimension: d { sql: ${c} ;; }
                dimension: e { sql: ${d}/${a} ;; }
                dimension: b { sql: ${a} ;; }
            }
        ''')
        # v.print_dependency_map()
        for i in v.e.ancestors():
            print(i.__refs__)

    def test_has_prop(self):
        x = lookml.Dimension('''
            dimension: x {
                description: "hello"
            }
        ''')
        self.assertTrue(x.hasProp('description'))
        self.assertFalse(x.hasProp('view_label'))

    def test_dependency_map(self):
        parsed_view = lkml.load(open('tests/files/the_look/views/01_order_items.view.lkml'))
        myView = lookml.View(parsed_view['views'][0])
        myView.print_dependency_map()
    
    def test_remove_fields(self):
        x = lookml.View('''
            view: x {
                dimension: a {}
                dimension: b { sql: IFNULL(${a},0) ;;}
                dimension: c { sql: ${a} ;; }
                dimension: x {}
                dimension: y {}
                dimension: z {}
                dimension: zz {}
            }
        ''')
        with self.assertWarns(UserWarning) as wrn:
            y = ['a','b','c']
            for i in y:
                x - i
            for w in wrn.warnings:
                self.assertTrue('a had dependencies:' in str(w))
        self.assertTrue('a' not in x)
        self.assertTrue('b' not in x)
        self.assertTrue('c' not in x)
        with self.assertWarns(UserWarning) as wrn:
            x - 'sql_table_name'
            for w in wrn.warnings:
                self.assertTrue('sql_table_name did not exist on x' in str(w))
        x + 'sql_table_name: order_items ;;'
        x - 'sql_table_name'
        x.removeField(x.x)
        x.removeField('y')
        x - x.z
        x - 'zz'
        self.assertTrue('x' not in x)
        self.assertTrue('y' not in x)
        self.assertTrue('z' not in x)
        self.assertTrue('zz' not in x)

    def test_set_name_safe(self):
        x = lookml.View('''
            view: x {
                dimension: a {}
                dimension: b { sql: NVL(${a}) ;;}
                dimension: c { sql: ${a} ;; }
            }
        ''')
        x.a.setName_safe('foo')
        x.foo.setName_replace_references('bar')
        self.assertTrue('bar' in x)
        self.assertTrue('${bar}' in x.b.sql.value)
        self.assertTrue('${bar}' in x.c.sql.value)

    #P3: message / comments
    # def test_messages_comments(self): pass

    def test_legacy_methods(self):
        x = lookml.View('''
            view: x {
                dimension: test456 {
                    type: number
                    tags: ["my_tag"]
                }
                dimension: test123 {
                    type: string
                }
                measure: a {}
                measure: b {}
                dimension: test789 {}
                filter: c {}
                filter: d {}
                parameter: z {}
                parameter: y {
                    tags: ["my_tag"]
                }
                dimension_group: created {}
            }
        ''')
        self.assertTrue('test456' in x)
        self.assertFalse('imnotthere' in x)
        #
        fieldNames = list()
        for i in x.fieldNames():
            fieldNames.append(i)
        result = ['test456','test123','test789','a','b','c','d','z','y','created']
        self.assertEqual(fieldNames,result)
        #
        testSort = list()
        for i in x.getFieldsSorted():
            testSort.append(i.name)
        result = ['c','created','d','test123','test456','test789','y','z','a','b']
        self.assertEqual(result, testSort)
        #
        filterList = list()
        for i in x.filters():
            filterList.append(i.name)
        result = ['c','d']
        self.assertEqual(result, filterList)
        #
        paramList = list()
        for i in x.parameters():
            paramList.append(i.name)
        result = ['z','y']
        self.assertEqual(result, paramList)
        #
        dimList = list()
        for i in x.dimensions():
            dimList.append(i.name)
        result = ['test456','test123','test789']
        self.assertEqual(result, dimList)
        #
        measList = list()
        for i in x.measures():
            measList.append(i.name)
        result = ['a','b']
        self.assertEqual(result, measList)
        #
        dimGroupList = list()
        for i in x.dimensionGroups():
            dimGroupList.append(i.name)
        result = ['created']
        self.assertEqual(result, dimGroupList)
        #
        byTagList = list()
        for i in x.getFieldsByTag('my_tag'):
            byTagList.append(i.name)
        result = ['test456','y']
        self.assertEqual(byTagList,result)
        #
        byTypeList = list()
        for i in x.getFieldsByType('string'):
            byTypeList.append(i.name)
        result = ['test123','test789','c','d','z','y']
        self.assertEqual(byTypeList,result)
        #
        x.addDimension('orderItemID')
        self.assertTrue('order_item_id' in x)
        testDim = lookml.Dimension('dimension: test_dim {}')
        x.addDimension(testDim)
        self.assertTrue('test_dim' in x)
        #
        x.addAverage(x.test456)
        self.assertTrue('test456_avg' in x)
        self.assertEqual(x.test456_avg.sql.value, '${x.test456}')
        #
        x.test123.setPrimaryKey()
        self.assertTrue(x._View__pk.name == 'test123')
        x.test123.setName('new')
        self.assertTrue(x._View__pk.name == 'new')
        x.new.unSetPrimaryKey()
        x.test456.setPrimaryKey()
        self.assertTrue(x._View__pk.name == 'test456')
        #
        x.new.setType('number')
        x.new.setDescription('this is my new dimension')
        new_view = lookml.View('''
        view: new_view {
            view_label: "hello"
        }
        ''')
        x.new.setViewLabel(new_view.view_label.value)
        self.assertEqual('hello',x.new.view_label.value)
        x.test456.setDBColumn( 'mycol', changeIdentifier=True)
        self.assertTrue('mycol' in x)
        self.assertEqual(x.mycol.sql.value,"${TABLE}.`mycol`")
        x.y.removeTag('my_tag')
        x.z.setString()
        x.a.addLink('http://yahoo.com{% condition foo %}{{value | uri_encode }}{% endcondition %}','Go to Yahoo')

    def test_new_file(self):
        pass

#P2: obtain the real list of timezones from Looker itself
#P3: add CLI support
#P3: option to omit defaults
#P3: add looker version numbers to the lang map and throw warning if prop depreicated or error if not yet supported

#P0: merge refinements that are present in a single file (currently only last)
# see tests/files/pylookml_test_project/models/queries_for_order_items.view.lkml

class testProjFile(unittest.TestCase):
    def setUp(self):
        pass
#Notes
#construct with github -> direct by default
#construct with github download="yes" -> download all
#construct with path = local, can attach SSH later? What would this look like
#construct with SSH downloads remote
#preserve legacy compatibility as much as possible
#don't the files change type based on project type?
# test new file of each type
    def pylookml_test_project_routine(self,proj):
        proj.dir_list()
        #loop through files
        for vf in proj.view_files():
            print(vf.name)
        #access a file's deep object via [] syntax
        val_a = proj['views/01_order_items.view.lkml']['views']['order_items']['order_id'].action[0].url.value
        self.assertEqual(val_a,'https://hooks.zapier.com/hooks/catch/1662138/tvc3zj/')
        #access a file's deep object via .file() syntax
        val_b = proj.file('views/01_order_items.view.lkml').views.order_items.order_id.action[0].url.value
        self.assertEqual(val_b,'https://hooks.zapier.com/hooks/catch/1662138/tvc3zj/')
        #mutate a file
        nf = proj.new_file('scratch/subfolder/pylookml_scratch.view.lkml')
        nf + lookml.View('''
            view: pylookml_scratch {
                dimension: test {}
            }
        ''')
        #write the file
        nf.write()
        #confirm write
        abc = proj.file('scratch/subfolder/pylookml_scratch.view.lkml')
        self.assertTrue('test' in abc.views.pylookml_scratch)
        #test optional pyyaml

    def test_project_from_local_path(self):

        #connect
        proj = project._project(
             local=True
            ,path='tests/files/pylookml_test_project'
            )
        # pprint.pprint(proj._index)
        self.pylookml_test_project_routine(proj)
        
        # x = proj['models/thelook.model.lkml']
        #P0: files in the top level folder
        # nf = proj.new_file('test.view.lkml')
        # nf + lookml.View('''
        #     view: new {
        #         dimension: id {}
        #     }
        # ''')
        # nf.write()
        # cool = proj['cool/cool.view.lkml']
        # cool.views.cool + '''
        #     dimension: rad {}
        # '''
        # cool.write()
        # trail_snap = proj['views/25_trailing_sales_snapshot.view.lkml']
        # print(trail_snap.views.inventory_snapshot)
        # print(x.datagroup.ecommerce_etl)
        # pprint.pprint(proj._index)
        # for f in proj:
        #     for v in f.views:
        #         print(v.name, v.sql_table_name)
        
        # for m in proj.model_files():
        #     print(m.connection.value)
        
        # for vf in proj.view_files():
        #     for v in vf.views:
        #         print(vf.path)
        #         print(' '*4, v.name) 
        
        # j = proj.new_file('cool/cool.view.lkml')
        # j + lookml.View('''
        #     view: cool {
        #         sql_table_name: public.cool ;;
        #         dimension: a {}
        #         dimension: b {}
        #         dimension: c {}
        #         dimension: d {}
        #         dimension: e {}
        #     }
        # ''')
        # j.views - 'cool'
        # print(j)
        # j.write()
        # a = proj.new_file('cool/cool.model.lkml')
        # a + lookml.Explore('''
        #     explore: cool {}
        # ''')
        # a + f'include: "{j.path}"'
        # print(a)
        # pprint.pprint(proj._index)
        # print(proj.file('views/04_products.view.lkml'))
        # print(j.path)


    def test_project_from_github(self):
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
        #P1: context manager for project

        # mf = proj.file('11_order_facts.view.lkml')
        # print(str(mf))

    def test_project_from_ssh(self):
        #connect
        proj = project._project(
             _git_url='git@github.com:pythonruss/pylookml_test_project.git'
            ,path='.tmp'
            ,_looker_project_name='pylookml_test_project'
            )
        self.pylookml_test_project_routine(proj)
        proj._git.add()
        proj.commit()
        proj._git.pushRemote()
        # proj.deploy()

        #iterate over files
        # proj.dir_list()
        # print(proj._looker_project_name)
        # print(proj._path)
        # print(proj._index)
        # i=0
        # for vf in proj.view_files():
        #     i+=1 
        # self.assertEqual(i,9)
        # self.assertEqual(proj['bike_share.model.lkml'].connection.value,"disco-parsec")




class testOtherFiles(unittest.TestCase):
    def setUp(self):
        pass

    def test_parsing_aggregate_tables(self):
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
        #works
        self.assertEqual(x.remote_dependency['ga360'].url.value,'https://github.com/llooker/google_ga360')
        self.assertEqual(x.remote_dependency.ga360.url.value,'https://github.com/llooker/google_ga360')
        # print(x.remote_dependency['ga360'])
        # print(x.remote_dependency.ga360)
        self.assertTrue('ga360' in x.remote_dependency)
        for remote in x.remote_dependency:
            print(remote.override_constant)
        
        # print(type(x.contents))
        #anon: local_dependency, visualization, 
        #named: constant, application, 
        #other props / project name etc 
        
        # print(str(x.contents))

    def test_dashboard_file(self):
        project.LOOKML_DASHBOARDS = True
        proj = project._project(
             local=True
            ,path='tests/files/the_look'
            )
        x = proj.file('dashboards/brand_lookup.dashboard.lookml')
        self.assertEqual(x.content[0]['dashboard'],'brand_lookup')
        #P1 fix writing, currently lookml dashboards should be considered read only
        x.content[0]['dashboard'] = 'foo'
        # x.write()

    def test_js_file(self):
        pass
    def test_json_file(self):
        pass

    def test_maplayer_topojson(self):
        pass

#P1: Looping through view.views poduces a [None]
# Explore source??

class testExceptions(unittest.TestCase):
    def setup(self): pass
    def test_invalid_lookml_attribute(self):
        with self.assertWarns(UserWarning) as wrn:
            testView = lookml.View({})
            testView.name = 'test'
            testView + '''
                dimension: foo {
                    xxx: "yyy"
                }
            '''
            # Verify
            for w in wrn.warnings:
                self.assertTrue('xxx skipped. xxx not a valid attribute' in str(w))

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




class testWalks(unittest.TestCase):
  def setUp(self):
      self.view = file.File('tests/files/basic_parsing/basic.view.lkml')

  def test_walking(self):
    for explore in self.view.explores:
      assert explore.name in ['basic']
      assert type(explore.join) == lookml.prop_named_construct

  def test_walk_explore(self):
    explore = self.view.explores.basic
    assert type(explore.join.cool) == lookml.prop_named_construct_single

  def test_walk_join(self):
    join = self.view.explores.basic.join.cool
    assert type(join) == lookml.prop_named_construct_single

    assert type(join.relationship) == lookml.prop_options
    assert join.relationship.value == 'many_to_one'
    
    assert type(join.type) == lookml.prop_options
    assert join.type.value == 'left_outer'
    
    assert type(join.sql_on) == lookml.prop_sql
    assert join.sql_on.value == '${basic.cool_id} = ${cool.basic_id}'
    # assert join.from == lookml.prop.string_unquoted

  def test_walk_view(self):
    view = self.view.views.basic
    assert type(view.extends) == lookml.prop_list_unquoted
    assert view.extends.value == ['base']

    assert type(view.extension) == lookml.prop_options
    assert view.extension.value == 'required'

    assert type(view.final) == lookml.prop_yesno
    assert view.final.value == 'no'

    assert type(view.label) == lookml.prop_string
    assert view.label.value == 'basic'

    assert type(view.view_label) == lookml.prop_string
    assert view.view_label.value == 'basic'

    assert type(view.required_access_grants) == lookml.prop_list_unquoted
    assert view.required_access_grants.value == ['a', 'b', 'c']

    assert type(view.suggestions) == lookml.prop_yesno
    assert view.suggestions.value == 'yes'

    assert type(view.derived_table) == lookml.prop_anonymous_construct

    for dim in view._dims():
      assert dim.name in ['foo', 'bar']

    assert type(view.transaction) == lookml.Dimension_Group

    for param in view._params():
      assert param.name in ['myparam']

    for measure in view._measures():
      assert measure.name in ['sum_foo', 'sum_bar']

  def test_walk_measure(self):
    measure = self.view.views.basic.sum_foo
    assert type(measure) == lookml.Measure
    assert measure.name == 'sum_foo'
    
    assert type(measure.type) == lookml.prop_options
    assert measure.type.value == 'sum'

    assert type(measure.sql) == lookml.prop_sql
    assert measure.sql.value == '${foo}'

    assert type(measure.filters) == lookml.prop_filters

  def test_walk_filters(self):
    filter = self.view.views.basic.sum_foo.filters.foo
    filter2 = self.view.views.basic.sum_bar.filters.foo

    assert type(filter) == lookml.flt
    assert filter.value == '%cool%'

    assert type(filter2) == lookml.flt
    assert filter2.value == '%cool%'

  def test_walk_dimension_group(self):
    dg = self.view.views.basic.transaction

    assert type(dg) == lookml.Dimension_Group
    assert dg.name == 'transaction'

    assert type(dg.type) == lookml.prop_options
    assert dg.type.value == 'time'

    assert type(dg.tags) == lookml.prop_list_quoted
    assert dg.tags.value == ['tag1', 'tag2', 'tag3', 'tag4']

    assert type(dg.timeframes) == lookml.prop_list_unquoted
    assert dg.timeframes.value == ['raw', 'time', 'date', 'week', 'month',
                                  'quarter', 'year', 'week_of_year', 'month_num']

    assert type(dg.sql) == lookml.prop_sql
    assert dg.sql.value == '${TABLE}.transaction_timestamp'

  def test_walk_dimension(self):
    dimension = self.view.views.basic.foo
    assert type(dimension) == lookml.Dimension

    assert type(dimension.type) == lookml.prop_options
    assert dimension.type.value == 'string'

    assert type(dimension.style) == lookml.prop_options
    assert dimension.style.value == 'classic'

    assert type(dimension.sql) == lookml.prop_sql
    assert dimension.sql.value == '${TABLE}.foo'

    assert type(dimension.link) == lookml.prop_anonymous_construct_plural

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
        # self.f = lookml.File('kitchenSink/kitchenSink.model.lkml')
        self.f = lookml.File('tests/files/kitchenSink/kitchenSink.model.lkml')
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
        # self.f_copy.views.order_items + 'test_add_dimension'
        self.f_copy.views.order_items.addDimension('test_add_dimension') #+ 'test_add_dimension'
        self.f_copy.views.order_items.shipping_time.setName_safe('time_in_transit')
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

    # def tearDown(self):
    #     '''
    #         remove KitchenSink2 if it exists (comment teardown out if having step6 difficulties and need to inspect kitchensink2)
    #     '''
    #     pass
        
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
        myNewView = lookml.View('great_test2').addDimension('id').addDimension('count_of_total')
        myNewView.id.sql = "${TABLE}.`id`"
        myNewView.id.setType('string')
        myNewFile = lookml.File(myNewView)
        proj.put(myNewFile)
        proj.deploy()

class whitespaceTest(unittest.TestCase):
    '''
        Test Procedure:
        Setup) Obtain Local Kitchen Sink Model File
        2) Parse the file
    '''
    # @unittest.skipIf(condition, reason)
    # @unittest.expectedFailure

    def setUp(self):
        self.f = lookml.File('tests/kitchenSink/kitchenSink.model.lkml')
        self.f2 = None
        self.order_items = self.f.views.order_items
        self.order_items_explore = self.f.explores.order_items

    def test_step0(self):
        print(self.order_items.id)

    def test_mvc(self):
        # x = lookml.View('order_items')
        # print(x.m.data)
        print(self.order_items)
        # print(self.order_items.m.data)

    def test_ws(self):
        f = lookml.File('tests/thelook/whitespace.view.lkml')
        print(f)
        
    def test_step1(self):
        for i in self.f.datagroups:
            print(i)
        o = self.order_items
        o.gross_margin.required_access_grants = ["a","b","c"]
        o.gross_margin.required_access_grants - 'a'
        o.gross_margin.required_access_grants + 'x'
        # for child in o.gross_margin.children():
        #     print(child)
        # o.gross_margin.sql = "${TABLE}.id"
        with self.assertRaises(Exception):
            o.gross_margin.sql + 'cool'
        # print([x for x in o.gross_margin.required_access_grants])
        # print(o.gross_margin)
        
        # for i in self.f.views.order_items.dims():
        #     print(i)

    def test_create_view_from_info_schema(self):
        def column_to_dimension(col):
            if col['LOOKER_TYPE'] == 'time':
                tmpDim = lookml.DimensionGroup(
                        lookml.lookCase(col['COLUMN_NAME'])
                        )
            else:
                tmpDim = lookml.Dimension(lookml.lookCase(col['COLUMN_NAME']))
            tmpDim.setType(col['LOOKER_TYPE'])
            tmpDim.sql = "${TABLE}." + col['COLUMN_NAME']
            return tmpDim

        sdk = init31("api.ini")
        sql = """
                SELECT 
                    t.TABLE_NAME
                    ,t.TABLE_SCHEMA
                    ,t.COLUMN_NAME
                    ,t.DATA_TYPE
                    , CASE 
                        WHEN t.DATA_TYPE IN ('TIMESTAMP_LTZ') THEN 'time'
                        WHEN t.DATA_TYPE IN ('FLOAT','NUMBER') THEN 'number'
                        ELSE 'string' END as "LOOKER_TYPE"
                FROM 
                    information_schema.COLUMNS as t
                WHERE
                    1=1
                    AND t.table_name = 'ORDER_ITEMS'
                    AND t.table_schema = 'PUBLIC'
                LIMIT 100
        """
        query_config = models.WriteSqlQueryCreate(sql=sql, connection_id="snowlooker")
        query = sdk.create_sql_query(query_config)
        response = sdk.run_sql_query(slug=query.slug, result_format="json")
        response_json = json.loads(response)
        order_items = lookml.View('order_items_3')
        order_items.sql_table_name = 'PUBLIC.ORDER_ITEMS'

        for column in response_json:
            order_items + column_to_dimension(column)

        order_items.sumAllNumDimensions()
        order_items.addCount()

        proj = lookml.Project(
                 repo= config['github']['repo']
                ,access_token=config['github']['access_token']
                ,looker_host="https://profservices.dev.looker.com/"
                ,looker_project_name="russ_sanbox"
        )
        myNewFile = lookml.File(order_items)
        proj.put(myNewFile)
        proj.deploy()

    def test_cool(self):
        v = lookml.View('cool')
        # v.properties.addProperty('derived_table',{'sql':'select 1'})
        v.derived_table = {'sql':'select 1'}
        # v.derived_table = {}
        # v.derived_table.sql = "select 2"
        # v.derived_table.datagroup_trigger = 'etl_24_hour'
        print(v)
        
    def test_refinement(self):
        exp = lookml.Explore('exp')
        lookml.mkdir_force('.tmp/scratch')
        with open('.tmp/scratch/refinement_test.model.lkml', 'w') as f:
            f.write(
                '''explore: refine_ex {}'''
            )
        myFile = lookml.File('.tmp/scratch/refinement_test.model.lkml')
        refine_ex = myFile.exps.refine_ex
        print(type(refine_ex))
        # refine_ex.addProperty('aggregate_table',{'materialization':{'datagroup_trigger':'orders_datagroup'}})
        print(refine_ex)
        # refine_ex.addProperty('aggregate_table','foo')
        print(myFile)


class testShellGitController(unittest.TestCase):
    '''
        Objective: test project instantiation and file crud, add commit
    '''

    def setUp(self):
        self.proj = lookml.Project(
                #  repo= config['github']['repo']
                # ,access_token=config['github']['access_token']
                 git_url='git@github.com:llooker/russ_sandbox.git'
                ,looker_host="https://profservices.dev.looker.com/"
                ,looker_project_name="russ_sanbox"
        )

    def test_step1(self):

        ## Do Work ###
        myNewView = lookml.View('great_test55').addDimension('id').addDimension('count_of_total')
        # myNewView = lookml.View('great_test55') + 'id' + 'count_of_total'
        myNewView.id.sql = "${TABLE}.`id`"
        myNewView.id.setType('string')
        myNewFile = lookml.File(myNewView)
        myNewFile.setFolder(self.proj.gitControllerSession.absoluteOutputPath)
        myNewFile.write()

    #     myNewFile = lookml.File(order_items)
    #     proj.put(myNewFile)
    #     proj.deploy()

        myOldFile = lookml.File('.tmp/russ_sanbox/02_users.view.lkml')
        myOldFile.views.users.hello.setType("number")
        myOldFile.write()

        ## Deploy ###
        self.proj.gitControllerSession.add().commit().pushRemote()

    def test_step2(self):
        for f in self.proj.files('simple'):
            print(f.path)

        # print(self.proj.file('simple/tests.view.lkml'))
        tests = self.proj.file('simple/tests.view.lkml') 
        tests + lookml.View('shell')
        tests.views.test1.bar.sql = 'WHOA'
        # tests.write()
        self.proj.update(tests)
        x = lookml.View('hello_world') 
        x + 'dimension: id {}'
        xf = lookml.File(x)
        self.proj.put(xf)
        self.proj.delete(xf)
        self.proj.deploy()

    def test_extends_bug(self):
        cool = lookml.View('cool')
        cool + 'extends: [wut]'
        print(cool)
        

class testMicroUnits(unittest.TestCase):

    def test_filtered_measure(self):
        meas = lookml.Measure('total_money')
        meas.setProperty('group_label','foo')
        # meas.properties.addProperty('filters',{'field':'order_items.price','value':'>100'})
        # meas.setProperty('filters',[{'field':'order_items.price','value':'>100'}])
        meas +  ('filters: { field: order_items.price value:">' + str(5) + '" }')
        meas.setViewLabel('test_viewLabel')
        # print(filt)
        # meas + filt
        print(meas)

    def test_add_micro_units(self):
        testView = lookml.View('testView')
        testView + 'id'
        testView + 'dimension: success {}'
        testView + '''
                derived_table: {
                    explore_source: order_items {
                    column: order_id {field: order_items.order_id_no_actions }
                    column: items_in_order { field: order_items.count }
                    column: order_amount { field: order_items.total_sale_price }
                    column: order_cost { field: inventory_items.total_cost }
                    column: user_id {field: order_items.user_id }
                    column: created_at {field: order_items.created_raw}
                    column: order_gross_margin {field: order_items.total_gross_margin}
                    derived_column: order_sequence_number {
                        sql: RANK() OVER (PARTITION BY user_id ORDER BY created_at) ;;
                    }
                    }
                    datagroup_trigger: ecommerce_etl
                }
        '''
        print(testView)

    def test_adding_property(self):
        v = lookml.View('test')
        v + '''
                derived_table: {
                    explore_source: order_items {
                    column: order_id {field: order_items.order_id_no_actions }
                    column: items_in_order { field: order_items.count }
                    column: order_amount { field: order_items.total_sale_price }
                    column: order_cost { field: inventory_items.total_cost }
                    column: user_id {field: order_items.user_id }
                    column: created_at {field: order_items.created_raw}
                    column: order_gross_margin {field: order_items.total_gross_margin}
                    derived_column: order_sequence_number {
                        sql: RANK() OVER (PARTITION BY user_id ORDER BY created_at) ;;
                    }
                    }
                    datagroup_trigger: ecommerce_etl
                }
        '''
        v + 'dimension: id {}'
        v.id + 'sql: ${TABLE}.id ;;'
        for item in ('a', 'b', 'c'):
            v + f'''
                dimension: {item}_id {{ 
                        sql: {v.id.__refs__} + {item} ;;
                    }}'''

            v + f'''measure: sum_of_{item} {{
                type: sum
                sql: ${{{item}_id}};;
            }}
            '''
        for f in v.measures():
            if f.type.value == 'sum':
                f.addTag('my function is to add') 
        
        ex = lookml.Explore(v.name)
        ex + '''join: test_2 {
                    from: test
                    type: left_outer
                    relationship: one_to_many
                    sql_on: ${testid} = ${test_2.id};;
                 }
        '''
        ex.test_2 + 'sql_on: foo ;;'
        F = lookml.File(ex)
        F + v
        print(F)

    def test_join_back_an_ndt(self):
        v = lookml.View('order_items')
        v + '''
            sql_table_name: public.order_items ;;
            dimension: id {
                primary_key: yes
            }
            dimension: state {}
            dimension: sale_price {}
            parameter: {dynamic_dim_selector} {
                type: unquoted
            #     suggestions: ["Brand","Category","Department"]
                allowed_value: {
                label: "Category"
                value: "Category"
                }
                allowed_value: {
                label: "Brand"
                value: "Brand"
                }
                allowed_value: {
                label: "Department"
                value: "Department"
                }
                allowed_value: {
                label: "State"
                value: "State"
                }
            }
            dimension: user_id {}
            dimension: inventory_item_id { 
                sql: ${TABLE}.inventory_item_id ;; 
            }
            dimension: new_dimension {
                type: string
                sql:
                    {% if order_items.dynamic_dim_selector._parameter_value == 'Brand' %} ${products.brand}
                    {% elsif order_items.dynamic_dim_selector._parameter_value == 'Category' %}  ${products.category}
                    {% elsif order_items.dynamic_dim_selector._parameter_value == 'Department' %} ${products.department}
                    {% elsif order_items.dynamic_dim_selector._parameter_value == 'State' %} ${users.state}
                    {% else %} 'N/A'
                    {% endif %}
                ;;
            }
            measure: total_sale_price {
                type: sum
                sql: ${sale_price} ;;
            }
        '''
        ex = lookml.Explore(v.name)
        agg = lookml.View('agg')
        agg + '''
                derived_table: {
                    explore_source: order_items {
                    column: new_dimension {field: order_items.new_dimension}
                    column: total_sale_price {field: order_items.total_sale_price}
                    derived_column: rank {
                        sql: ROW_NUMBER() OVER (ORDER BY total_sale_price DESC) ;;
                    }
                    # bind_all_filters: yes
                    bind_filters: {
                        from_field: order_items.{dynamic_dim_selector}
                        to_field: order_items.{dynamic_dim_selector}
                    }
                    # bind_filters: {
                    #     from_field: order_items.created_date
                    #     to_field: order_items.created_date
                    # }
                    }
                }
                dimension: new_dimension {
                    sql: ${TABLE}.new_dimension ;;
                }
                dimension: rank {
                    type: number
                    hidden: yes
                }

                filter: tail_threshold {
                    type: number
                    hidden: yes
                }

                dimension: stacked_rank {
                    type: string
                    sql:
                            CASE
                            WHEN ${rank} < 10 then '0' || ${rank} || ') '|| ${new_dimension}
                            ELSE ${rank} || ') ' || ${new_dimension}
                            END
                    ;;
                }

                dimension: ranked_brand_with_tail {
                    type: string
                    sql:
                        CASE WHEN {% condition tail_threshold %} ${rank} {% endcondition %} THEN ${stacked_rank}
                        ELSE 'x) Other'
                        END

                    ;;
                }

                dimension: total_sale_price {
                    value_format: "$#,##0.00"
                    type: number
                }
        '''

        ex + '''
            join: inventory_items {
                type: left_outer
                relationship: one_to_many
                sql_on: ${order_items.inventory_item_id} = ${inventory_items.id} ;;
            }
            join: products {
                type: left_outer
                sql_on: ${inventory_items.product_id} = ${products.id} ;;
                relationship: many_to_one
            }
              join: users {
                type: left_outer
                sql_on: ${order_items.user_id} = ${users.id} ;;
                relationship: many_to_one
                      }
              join: agg {
                type: left_outer
                relationship: many_to_one
                sql_on: ${order_items.new_dimension}  = ${agg.new_dimension};;
            }
        '''
        myModel = lookml.File(ex)
        myModel + v
        myModel + agg
        myModel.properties.addProperty('connection', 'snowlooker')
        myModel.properties.addProperty('include', 'views/*.lkml')
        myModel.name = 'core2.model.lkml'
        proj = lookml.Project(
                 repo= 'russlooker/oi'
                ,access_token=config['github']['access_token']
                ,looker_host="https://profservices.dev.looker.com/"
                ,looker_project_name="test_pylookml"
        )

        proj.put(myModel)
        proj.deploy()

    def test_one_line_access_github(self):
        print(   
        lookml.Project(**config['project1'])['order_items.view.lkml']['views']['order_items']['id'].primary_key.value
        # lookml.Project(**config['project1']).file('order_items.view.lkml').views.order_items.id.primary_key.value
        )

    def test_topN(self):
        def apply_top_n(project, view_file, view, rank_by_dims, rank_by_meas, model_file, explore, agg_view='rank_ndt', dynamic_dim_name='dynamic_dim', dynamic_dim_selector='dynamic_dim_selector'):
            #### SETUP ####
            p = project
            mf = p[model_file]
            vf = p[view_file]
            v = vf['views'][view]
            e = mf['explores'][explore]
            #### DO WORK ####
            #Add the parameter to the initial view file
            dynamic_dim_sql = ''
            i = 0
            for key,val in rank_by_dims.items():
                if i == 0:
                    dynamic_dim_sql = f"{{% if {v.name}.{dynamic_dim_selector}._parameter_value == '{key}' %}} {val}"
                else:
                    dynamic_dim_sql = dynamic_dim_sql + '\n' + f"{{% elsif {v.name}.{dynamic_dim_selector}._parameter_value == '{key}' %}} {val}"
                i = 1 + 1
            dynamic_dim_sql = dynamic_dim_sql + f"""
                    {{% else %}} 'N/A' 
                    {{% endif %}}
                """
            allowed_values = ''
            for key in rank_by_dims.keys():
                allowed_values = allowed_values + f'allowed_value: {{ label: "{key}" value: "{key}"}}'

            v + f'''
                parameter: {dynamic_dim_selector} {{
                    type: unquoted

                    {allowed_values}
                }}'''

            v + f'''
                dimension: {dynamic_dim_name} {{
                    type: string
                    hidden: yes
                    sql: {dynamic_dim_sql};;
                }}

            '''
            #create the aggregate ndt
            agg = lookml.View(agg_view)
            agg + f'''
                derived_table: {{
                    explore_source: {e.name} {{
                    column: {dynamic_dim_name} {{field: {v.name}.{dynamic_dim_name}}}
                    column: {rank_by_meas} {{field: {v.name}.{rank_by_meas}}}
                    derived_column: rank {{
                        sql: ROW_NUMBER() OVER (ORDER BY {rank_by_meas} DESC) ;;
                    }}
                    # bind_all_filters: yes
                    bind_filters: {{
                        from_field: {v.name}.{dynamic_dim_selector}
                        to_field: {v.name}.{dynamic_dim_selector}
                    }}
                    }}
                }}
                dimension: {dynamic_dim_name} {{
                    sql: ${{TABLE}}.{dynamic_dim_name} ;;
                    hidden: yes
                }}
                dimension: rank {{
                    type: number
                    hidden: yes
                }}
                filter: tail_threshold {{
                    type: number
                    hidden: yes
                }}
                dimension: stacked_rank {{
                    type: string
                    sql:
                            CASE
                            WHEN ${{rank}} < 10 then '0' || ${{rank}} || ') '|| ${{{dynamic_dim_name}}}
                            ELSE ${{rank}} || ') ' || ${{{dynamic_dim_name}}}
                            END
                    ;;
                }}
                dimension: ranked_by_with_tail {{
                    type: string
                    sql:
                        CASE WHEN {{% condition tail_threshold %}} ${{rank}} {{% endcondition %}} THEN ${{stacked_rank}}
                        ELSE 'x) Other'
                        END
                    ;;
                }}
            '''
            #add our new aggregate view to the view file
            vf + agg
            #join in our aggregate table to the explore
            e + f'''
              join: {agg.name} {{
                type: left_outer
                relationship: many_to_one
                sql_on: ${{{v.name}.{dynamic_dim_name}}}  = ${{{agg.name}.{dynamic_dim_name}}};;
             }}
            '''

            #### SAVE ####
            p.put(vf)
            p.put(mf)
            p.deploy()



        apply_top_n(
             lookml.Project(**config['project1'])
            ,'order_items.view.lkml' #ordinarily should be my view file
            ,'order_items'
            ,{'Brand':'${products.brand}','Category':'${products.category}','State':'${users.state}'}
            ,'total_sale_price'
            ,'order_items.model.lkml' 
            ,'order_items'
            )

    def test_local_file(self):
        x = lookml.File('lookml/tests/kitchenSink/kitchenSink.model.lkml')
        for v in x.views:
            for f in v.measures():
                if f.type.value == 'sum' and not f.name.endswith('_total'):
                    f.name = f.name + '_total'
        #Optionally Change the location
        x.setFolder('.tmp')
        #Write the file
        x.write()

    def test_model_file_creation(self):
        #initialize project
        #create new model file
        #put and check output
        pass

    def test_parse_references(self):
        results = list(lookml.parseReferences('''
            ${test.one_1} - ${test.two}
            {% condition test.three %} ${four} {% endcondition %}
            {% parameter test.five %}
            {{ six }}
            {{seven}}
            {{test.eight}}
            {{ _filters['test.nine'] | url_encode}}
            {% _filters['ten10'] %}
        '''))
        self.assertEqual(results[0]['field'],'test.one_1')
        self.assertEqual(results[1]['field'],'test.two')
        self.assertEqual(results[2]['field'],'test.three')
        self.assertEqual(results[3]['field'],'four')
        self.assertEqual(results[4]['field'],'test.five')
        self.assertEqual(results[5]['field'],'six')
        self.assertEqual(results[6]['field'],'seven')
        self.assertEqual(results[7]['field'],'test.eight')
        self.assertEqual(results[8]['field'],'test.nine')
        self.assertEqual(results[9]['field'],'ten10')
        self.assertEqual(results[9]['fully_qualified_reference'],False)

    def test_field_deletion(self):
        self.proj = lookml.Project(
                #  repo= config['github']['repo']
                # ,access_token=config['github']['access_token']
                 git_url='git@github.com:llooker/russ_sandbox.git'
                ,looker_host="https://dat.dev.looker.com/"
                ,looker_project_name="pylookml"
        )
        viewFile = self.proj.file('01_order_items.view.lkml')
        view = viewFile['views']['order_items'] 
        for f in view.fields():
            if f.name not in ('id'):
                view - f
        print(view)
        # or alternatively remove the fields with a loop
        # for field in viewFile.fields():
            # if field.name in ('count','sales_price'):
        
        # viewFile.removeField(field)

    def test_project_level_functions(self):
        self.proj = lookml.Project(
                #  repo= config['github']['repo']
                # ,access_token=config['github']['access_token']
                 git_url='git@github.com:llooker/russ_sandbox.git'
                ,looker_host="https://dat.dev.looker.com/"
                ,looker_project_name="pylookml"
        )
        self.proj.buildIndex()

    def test_new_filters(self):
        test = lookml.View('test')
        test2 = lookml.View('+test')
        test + "dimension: foo {}"
        test2 + "dimension: bar {}"
        x = lookml.File(test)
        x.setFolder('.')
        x + test2
        x.write()
        print(x.path)
        # print(x)
        # print(lookml.l('measure: { filters:[a:"b",c:"d"] }'))
        print(lookml.l(str(x)))

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

class testModel(unittest.TestCase):
  def setUp(self):
      self.model = file.File('tests/files/basic_parsing/basic.model.lkml')
      self.explore_names = ['trip', 'station_weather_forecast', 'station_forecasting']

  def test_walking(self):
    for explore in self.model:
      assert explore.name in self.model.explores
      assert isinstance(explore.join, lookml.prop_named_construct)

  def test_walk_explore(self):
    explore = self.model.explores.trip
    assert type(explore.join.start_station) == lookml.prop_named_construct_single

    explore2 = self.model.explores.station_weather_forecast
    assert type(explore2.hidden) == lookml.prop_yesno
    assert explore2.hidden.value == 'yes'
    assert type(explore.view_name) == lookml.prop_string_unquoted
    assert explore2.view_name.value == 'weather_forecast'
    
    # assert explore2.from == lookml.prop.string_unquoted

  def test_walk_join(self):
    join = self.model.explores.trip.join.start_station
    assert type(join) == lookml.prop_named_construct_single
    assert type(join.relationship) == lookml.prop_options
    assert join.relationship.value == 'many_to_one'
    assert type(join.type) == lookml.prop_options
    assert join.type.value == 'left_outer'
    assert type(join.sql_on) == lookml.prop_sql
    assert join.sql_on.value == '${trip.from_station_id} = ${start_station.station_id}'
    # assert join.from == lookml.prop.string_unquoted

class testConnectivity(unittest.TestCase):
    '''
        objective: 
            Test coverage on all the methods of interacting with external services
            github (access_token)
            ssh git interaction
            Local filesystem
            Looker API 
            Looker deploy webhook
            success criteria: 
            need to successfully connect, perform multiple operations CRUD, then reconnect and parse again
    '''
    def setUp(self):
        pass

    def test_local_filesystem(self):
        pass
    def test_github_connection(self):
        pass
    def test_ssh_git_connection(self):
        pass
    def test_looker_api(self):
        pass
    def test_looker_deploy_webhook(self):
        pass
    def tearDown(self):
        pass