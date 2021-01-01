import src.lookml.lookml as lookml
import src.lookml.lkml as lkml

import unittest, copy
from pprint import pprint
import configparser, json
# from looker_sdk import client, models, methods
from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('tests/settings.ini')

class testScenarioEAV(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        pass
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



 



    