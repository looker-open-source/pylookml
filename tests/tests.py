import unittest, copy
import lookml
import configparser, json
from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('settings.ini')

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
        # self.f_copy.views.order_items + 'test_add_dimension'
        self.f_copy.views.order_items.addDimension('test_add_dimension') #+ 'test_add_dimension'
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
        self.f = lookml.File('lookml/tests/kitchenSink/kitchenSink.model.lkml')
        self.f2 = None
        self.order_items = self.f.views.order_items
        self.order_items_explore = self.f.explores.order_items

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

# TODO: Write a test that would use materialization and refinements
# Meterialization:
# explore: event {
#   aggregate_table: monthly_orders {
#     materialization: {
#       datagroup_trigger: orders_datagroup
#     }
#     query: {
#       dimensions: [orders.created_month]
#       measures: [orders.count]
#       #filters: [orders.created_date: "1 year", orders.status: "fulfilled"]
#       filters: {
#           field: orders.created_date
#           value: "1 year"
#           }
#       filters: {
#           field: orders.status
#           value: "fulfilled"
#           }
#       timezone: "America/Los_Angeles"
#     }
#   }
# }



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

    # def test_derived_table_object_access_and_whitespace(self):
    #     v = lookml.View('v')
    #     v + '''
    #         derived_table: {
    #             explore_source: x {
    #                 column: a { field: a.cool }
    #                 column: b {field: b.cool }
    #                 derived_column: c { sql: foo! ;;}
    #             }
    #         }
    #     '''
    #     # print(v)
    #     # print(v)
    #     # v.derived_table = {}
    #     # print(v)

    def test_eav_unnester(self):
        sdk = init31("api.ini")
        sql_for_fields = f"""
                SELECT 
                     cpf.org_id
                    ,cpf.value
                    ,cpf.datatype
                    ,cpf.field_name as "FIELD_NAME"
                    , CASE 
                        WHEN cpf.datatype IN ('TIMESTAMP_LTZ') THEN 'time'
                        WHEN cpf.datatype IN ('FLOAT','NUMBER', 'int') THEN 'number'
                        ELSE 'string' END as "LOOKER_TYPE"
                FROM 
                    -- public.custom_profile_fields as cpf
                    (
                        SELECT 1 as user_id, 8 as org_id, 'c_donation_amount' as field_name, '40' as value, 'int' as datatype UNION ALL
                        SELECT 1, 8, 'c_highest_achievement', 'gold badge', 'varchar' UNION ALL
                        SELECT 2, 101, 'c_highest_achievement', 'silver badge', 'varchar' UNION ALL
                        SELECT 2, 101, 'c_monthly_contribution', '300', 'int' UNION ALL
                        SELECT 3, 101, 'c_highest_achievement', 'bronze badge', 'varchar' UNION ALL
                        SELECT 3, 101, 'c_monthly_contribution', '350', 'int' UNION ALL
                        SELECT 4, 101, 'c_monthly_contribution', '350', 'int' UNION ALL
                        SELECT 4, 101, 'age', '32', 'int' UNION ALL
                        SELECT 5, 102, 'c_monthly_contribution', '100', 'int'
                    ) as cpf
                WHERE
                    1=1
                GROUP BY 1,2,3,4,5
                LIMIT 100
        """
        query_config = models.WriteSqlQueryCreate(sql=sql_for_fields, connection_id="snowlooker")
        query = sdk.create_sql_query(query_config)
        response = json.loads(sdk.run_sql_query(slug=query.slug, result_format="json"))

        proj = lookml.Project(
                 repo= config['github']['repo']
                ,access_token=config['github']['access_token']
                ,looker_host="https://profservices.dev.looker.com/"
                ,looker_project_name="russ_sanbox"
                ,branch='dev-russell-garner-b7gj'
        )

        modelFile = proj['eav_example/eav.model.lkml']

        eavSource = modelFile['views']['eav_source']
        flatteningNDT = modelFile['views']['usr_profile']

        #Step 0) Ensure there is a hidden explore to expose the eav_souce for NDT
        modelFile + f'''
            explore: _eav_flattener {{
                from: {eavSource.name}
                hidden: yes
            }}
        '''
        #Begin the derived table, will be added to as we loop through the fields
        drivedtableString = f'''
            derived_table: {{
                explore_source: _eav_flattener {{
                    column: user_id {{ field: _eav_flattener.user_id }}
                    column: org_id {{ field: _eav_flattener.org_id }}
        '''

        #Set up a list to track the unique org ids and column names
        orgIds, columns = [], []

        for column in response:
            dimName = lookml.lookCase(column['FIELD_NAME'])
            orgIds.append(column['ORG_ID'])
            columns.append(dimName)
            #Step 1) Add flattening measure to the EAV source table
            eavSource + f'''
                  measure: {dimName} {{
                        type: max
                        sql: CASE WHEN ${{field_name}} = '{column['FIELD_NAME']}' THEN ${{value}} ELSE NULL END;;
                    }}
            '''

            #Step 2) Add to the NDT fields
            flatteningNDT + f'''
                    dimension: {dimName}_org_{column['ORG_ID']} {{
                        label: "{dimName}"
                        type: {column['LOOKER_TYPE']}
                        sql: ${{TABLE}}.{dimName} ;;
                        required_access_grants: [org_{column['ORG_ID']}]
                    }}
            '''
            if column['LOOKER_TYPE'] == "number":
                flatteningNDT + f'''
                    measure: {dimName}_total_org_{column['ORG_ID']} {{
                        label: "{dimName}_total"
                        type: sum
                        sql: ${{{dimName}_org_{column['ORG_ID']}}} ;;
                        required_access_grants: [org_{column['ORG_ID']}]
                    }}
                '''
        #Finalize / add the completed derived table string to the NDT:
        for col in set(columns):
            drivedtableString += f' column: {col} {{ field: _eav_flattener.{col} }}'
        drivedtableString += '}}'

        #Create the access grants for each org
        accessGrants = ''
        for org in set(orgIds):
            accessGrants += f'''
                access_grant: org_{org} {{
                user_attribute: org_id
                allowed_values: [
                    "{org}"
                ]
                }}
            '''

        #Finish by adding the derived table to the 
        flatteningNDT + drivedtableString
        modelFile + accessGrants

        proj.put(modelFile)
        # proj.deploy()


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






if __name__ == '__main__':
    unittest.main()