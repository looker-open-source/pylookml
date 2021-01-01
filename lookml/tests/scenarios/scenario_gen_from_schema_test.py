
import src.lookml.lookml as lookml
import src.lookml.lkml as lkml
import unittest, copy
from pprint import pprint
import configparser, json
# from looker_sdk import client, models, methods
from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('settings.ini')

class testScenariosGenerateFromSchema(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        pass
    
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

        sdk = init31("tests/api.ini")
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

    def tearDown(self):
        pass