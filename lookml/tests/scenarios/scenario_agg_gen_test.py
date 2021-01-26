
import src.lookml.lookml as lookml
import src.lookml.project as project
import src.lookml.lkml as lkml

import unittest, copy, re, sys
from pprint import pprint
import configparser, json
import looker_sdk
from looker_sdk import models, methods, init31
config = configparser.ConfigParser()
config.read('tests/settings.ini') 

class testScenariosAggGen(unittest.TestCase):
    '''
        Objective: test end to end common use case scenarios 
    '''
    def setUp(self):
        self.sdk = looker_sdk.init40("tests/api.ini")

    def test_dimension_add(self):
        x = lookml.Explore('''
        explore: foo {
            aggregate_table: auto_pylookml_NBDM6pP {
                query: {       
                dimensions: []      
                measures: []      
                description: ""      
                filters: [  ]       
                limit: 5000
                }
                materialization: {       
                sql_trigger_value: select 1 ;;
                } }
                }
        ''')
        x.aggregate_table['auto_pylookml_NBDM6pP'].query.dimensions + 'foo'
        filt = {'mock_data_aa.feature_clean': '"Login_Login"'}
        filt = {k:v[1:][:-1] for k,v in filt.items()}
        x.aggregate_table['auto_pylookml_NBDM6pP'].query.filters + filt
        print(x)

    def test_generate_aggregate_table(self):
        frequent_queries = self.sdk.run_inline_query(result_format='json',body={
                    "model":"system__activity",
                    "view": "history",
                    "fields": [
                        "query.model",
                        "query.view",
                        "query.formatted_fields",
                        "query.filters",
                        "query.slug",
                        "history.query_run_count",
                        "history.max_runtime",
                        "history.average_runtime"
                    ],
                    "filters": {
                        "query.model": "-NULL,-\"system__activity\""
                    },
                    "sorts": [
                        "history.query_run_count desc"
                    ],
                    "limit": "10"
                })
        frequent_queries = json.loads(frequent_queries)
        field_type_index = dict()
        for query in frequent_queries:
            #look up the model attributes
            model = self.sdk.lookml_model(query["query.model"])
            #look up the project attributes
            looker_project = self.sdk.project(model.project_name)
            if looker_project.git_service_name == 'github' and looker_project.name == 'dbs':
                git_search = re.search(
                    r'git@github.com:([a-zA-Z0-9_]{1,100}\/[a-zA-Z_0-9]{1,100})\.git', 
                    looker_project.git_remote_url)
                if git_search:
                    repo = git_search.group(1)
                do = 0
                if looker_project.name not in field_type_index.keys():
                    do = 1
                    field_type_index[looker_project.name] = {}
                if query["query.model"] not in field_type_index[looker_project.name].keys():
                    do = 1
                    field_type_index[looker_project.name][query["query.model"]] = {}
                if query["query.view"] not in field_type_index[looker_project.name][query["query.model"]].keys():
                    do = 1
                    field_type_index[looker_project.name][query["query.model"]][query["query.view"]] = {
                         'dimensions':[]
                        ,'measures':[]
                        }
                if do:
                    metadata = self.sdk.lookml_model_explore(query["query.model"], query["query.view"],fields='fields')
                    for dimension in metadata.fields.dimensions:
                        field_type_index[looker_project.name][query["query.model"]][query["query.view"]]['dimensions'].append(dimension.name)
                    for measure in metadata.fields.measures:
                        field_type_index[looker_project.name][query["query.model"]][query["query.view"]]['measures'].append(measure.name)
                try:
                    pylookml_project = project.Project(
                         repo= repo
                        ,access_token=config['project1']['access_token']
                        ,looker_host='https://dat.dev.looker.com/'
                        ,looker_project_name=looker_project.name
                    )
                    #P1: we can't assume the file path, what if in subfolder?
                    pylookml_model = pylookml_project[query["query.model"]+'.model.lkml']
                    #P1: we can't assume all explores are in the model file
                    # lookml_model_explore has the filesystem location {
                    # "source_file": "dbs.model.lkml"
                    # }
                    pylookml_explore = pylookml_model.explores[query["query.view"]]
                    # {query["query.slug"]} 
                    pylookml_explore + f'''
                        aggregate_table: auto_pylookml_{query["query.slug"]} {{
                            query: {{
                                dimensions: []
                                measures: []
                                description: "https://dat.dev.looker.com/x/{query["query.slug"]}"
                                filters: []
                                limit: 5000
                                }}
                            materialization: {{
                                sql_trigger_value: select 1 ;;
                                }}
                        }}
                    '''
                    fields = json.loads(query["query.formatted_fields"])
                    for field in fields:
                        if field in field_type_index[looker_project.name][query["query.model"]][query["query.view"]]["dimensions"]:
                            pylookml_explore.aggregate_table["auto_pylookml_"+query["query.slug"]].query.dimensions + field
                        if field in field_type_index[looker_project.name][query["query.model"]][query["query.view"]]["measures"]:
                            pylookml_explore.aggregate_table["auto_pylookml_"+query["query.slug"]].query.measures + field
                    filters = json.loads(query["query.filters"])
                    #P1: aggregate tables can't take paramter fields. Need to ensure each filter is not a param
                    pylookml_explore.aggregate_table["auto_pylookml_"+query["query.slug"]].query.filters + {k:v[1:][:-1] for k,v in filters.items()}
                    pylookml_project.put(pylookml_model)
                    #P1: put a https://dat.dev.looker.com/x/<<slug>> in the description
                except:
                    print("Unexpected error:", sys.exc_info()[0])


    def tearDown(self):
        pass

