import click
import looker_sdk
import lookml
import os, re, sys, json
import configparser
import time
from lookml.lib.utils import url

def init_looker_sdk(
        url:str, 
        client_id:str, 
        client_secret:str, 
        version:str='4.0') -> looker_sdk.methods40.Looker40SDK:
    os.environ['LOOKERSDK_BASE_URL'] = url
    os.environ['LOOKERSDK_CLIENT_ID'] = client_id
    os.environ['LOOKERSDK_CLIENT_SECRET'] = client_secret
    os.environ['LOOKERSDK_VERIFY_SSL'] = 'true'
    os.environ['LOOKERSDK_TIMEOUT'] = '120'
    os.environ['LOOKERSDK_API_VERSION'] = '4.0'
    return looker_sdk.init40()

def routine(
         access_token
        ,looker_host
        ,api_client
        ,api_secret
        ,model_name
        ,branch
    ):
    looker_host=url(looker_host)
    sdk = init_looker_sdk(looker_host.with_port_if_exists(), api_client, api_secret)
    frequent_queries = sdk.run_inline_query(
                result_format='json',
                body={
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
                        # "query.model": f"-NULL,-\"system__activity\",{model_name}"
                        "query.model": f"{model_name}"
                    },
                    "sorts": [
                        "history.query_run_count desc"
                    ],
                    "limit": "100"
            })
    frequent_queries = json.loads(frequent_queries)
    click.echo("working on branch: " + branch)
    #look up the model attributes
    model = sdk.lookml_model(model_name)
    #look up the project attributes
    looker_project = sdk.project(model.project_name)
    if looker_project.git_service_name == 'github': 
        git_search = re.search(
            r'git@github.com:([a-zA-Z0-9_]{1,100}\/[a-zA-Z_0-9]{1,100})\.git', 
            looker_project.git_remote_url)
        if git_search:
            repo = git_search.group(1)

    pylookml_project = lookml.Project(
        repo= repo
        ,access_token=access_token
        ,looker_host=looker_host.with_no_port()+'/'
        ,looker_project_name=looker_project.name
        ,branch=branch
    )
    if pylookml_project._exists(f'pylookml/{model_name}_aggs.view.lkml'):
        # click.echo('passed exists check')
        f = pylookml_project.file(f'pylookml/{model_name}_aggs.view.lkml')
        # click.echo(f.sha)
    else:
        f = pylookml_project.new_file(f'pylookml/{model_name}_aggs.view.lkml')
    field_type_index = dict()
    #P1: we can't assume the file path, what if in subfolder?
    pylookml_model = pylookml_project[model_name+'.model.lkml']
    pylookml_model + f'includes: "pylookml/{model_name}_aggs.view"'
    #P1: we can't assume all explores are in the model file
    # lookml_model_explore has the filesystem location {
    # "source_file": "dbs.model.lkml"
    # }
    #P1: doesn't handle being run twice well
    with click.progressbar(frequent_queries) as fq:
        for query in fq:
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
                    metadata = sdk.lookml_model_explore(query["query.model"], query["query.view"],fields='fields')
                    for dimension in metadata.fields.dimensions:
                        field_type_index[looker_project.name][query["query.model"]][query["query.view"]]['dimensions'].append(dimension.name)
                    for measure in metadata.fields.measures:
                        field_type_index[looker_project.name][query["query.model"]][query["query.view"]]['measures'].append(measure.name)
                try:
                    
                    #P1 we don't need the explore technically since we're writing elsewhere
                    # pylookml_explore = pylookml_model.explores[query["query.view"]]
                    # {query["query.slug"]} 
                    # pylookml_explore + f'''
                    # click.echo(f'{query["query.view"]}')
                    explore_source_file_path = sdk.lookml_model_explore(
                            lookml_model_name=query["query.model"],
                            explore_name=query["query.view"],
                            fields='source_file'
                            )
                    explore_source_file = pylookml_project.file(explore_source_file_path.source_file)
                    pylookml_source_explore = explore_source_file.explores[query["query.view"]]
                    if 'persist_for' in pylookml_source_explore:
                        materialization = pylookml_source_explore.persist_for
                    elif 'persist_with' in pylookml_source_explore:
                        materialization = 'datagroup_trigger: ' + pylookml_source_explore.persist_with.value
                    elif 'persist_for' in explore_source_file:
                        materialization = explore_source_file.persist_for
                    elif 'persist_with' in explore_source_file:
                        materialization = 'datagroup_trigger: ' + explore_source_file.persist_with.value
                    else:
                        materialization = 'persist_for: "24 hours"'

                    f + 'include: "/**/*.model"'
                    if f'+{query["query.view"]}' not in f.explores:
                        f + f'''explore: +{query["query.view"]} {{ }}'''
                    f.explores['+' + query["query.view"]] + f'''
                        aggregate_table: auto_pylookml_{query["query.slug"]} {{
                            query: {{
                                dimensions: []
                                measures: []
                                description: "{looker_host.with_no_port()}/x/{query["query.slug"]}"
                                filters: []
                                }}
                            materialization: {{
                                {materialization}
                                }}
                            }}
                        '''
                    fields = json.loads(query["query.formatted_fields"])
                    for field in fields:
                        if field in field_type_index[looker_project.name][query["query.model"]][query["query.view"]]["dimensions"]:
                            f.explores['+'+query["query.view"]].aggregate_table["auto_pylookml_"+query["query.slug"]].query.dimensions + field
                        if field in field_type_index[looker_project.name][query["query.model"]][query["query.view"]]["measures"]:
                            f.explores['+'+query["query.view"]].aggregate_table["auto_pylookml_"+query["query.slug"]].query.measures + field
                    try:
                        if query["query.filters"]:
                            filters = json.loads(query["query.filters"])
                            click.echo(query["query.filters"] + ' | ' + filters)
                    except:
                        pass
                        # click.echo(f'failure with {query["query.filters"]}')
                    #P1: aggregate tables can't take paramter fields. Need to ensure each filter is not a param
                    if filters:
                        # f.explores['+'+query["query.view"]].aggregate_table["auto_pylookml_"+query["query.slug"]].query.filters + {k:v[1:][:-1] for k,v in filters.items()}
                        f.explores['+'+query["query.view"]].aggregate_table["auto_pylookml_"+query["query.slug"]].query.filters + {k:v for k,v in filters.items()}
                    # pylookml_model.write()
                    # pylookml_project.put(pylookml_model)
                except:
                    e = sys.exc_info()[0]
                    click.echo(f'Unexpected error: {e}')
    f.write()

        # except:
        #     click.echo(f'error, review your inputs and try again {sys.exc_info()[0]}')


@click.command()
# @click.option('--repository',  prompt='repo i.e. llooker/mycompany',help='github repo containing the project')
@click.option('--access_token',  prompt='your github access token',help='github personal access token')
@click.option('--looker_host',  prompt='looker host https://demo.looker.com/',help='looker host to work upon')
@click.option('--api_client',  prompt='Client ID',help='Looker API client ID')
@click.option('--api_secret',  prompt='API Secret Key',help='Looker API Secret')
@click.option('--model_name',  prompt='Looker Model Name',help='model to evaluate, i.e. hr_analytics')
@click.option('--branch',  prompt='git branch',help='master by default, can be your dev branch')
def guided(
         access_token 
        ,looker_host
        ,api_client
        ,api_secret
        ,model_name
        ,branch
        ):
    routine(
         access_token
        ,looker_host
        ,api_client
        ,api_secret
        ,model_name
        ,branch
    )

@click.command()
@click.option('--config_path',type=str,prompt='path to .ini file',help='')
def useconf(config_path):
    '''
    Your config should look like this:
    [autotune]
    access_token = xxx
    looker_host = https://mycompany.looker.com:19999
    api_client = xxx
    api_secret = yyy
    model_name = bike_share
    branch = dev-john-doe-yddt
    '''
    config = configparser.ConfigParser()
    # config.read('lookml/tests/settings.ini')
    config.read(config_path)
    routine(**config['autotune'])

@click.group(invoke_without_command=True)
def autotune():
    if os.path.exists('autotune.ini'):
        config = configparser.ConfigParser()
        config.read('autotune.ini')
        routine(**config['autotune'])
    else:
        pass


autotune.add_command(useconf)
autotune.add_command(guided)