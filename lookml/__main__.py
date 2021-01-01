#from lookml import core as lookml
import lookml
import click
import os
import looker_sdk
import json, re, sys
#P3 CLI show children report for a specific field
#P3 CLI change a dimension name safely
#P3 CLI create LookML from a well known artifact from another tool
#P3 CLI apply block
#P3 CLI auto-tune your Looker Instance (create aggregate tables for top queries)
# write logs to a file in cwd
#P3 CLI add sums & averages of all number dimensions 
@click.group()
def cli():
    pass

@click.command()
@click.option('--repository',  prompt='repo i.e. llooker/mycompany',help='github repo')
@click.option('--access_token',  prompt='your github access token',help='github access token')
def directory(repository, access_token):
    """Simple File Listing Capability"""
    proj = lookml.ProjectGithub(
         index_whole=True
        ,repo=repository
        ,access_token=access_token
    )
    proj.dir_list()

@click.command()
def doctree():
    '''
    Lists the parameter tree of LookML and links to documentation
    '''
    _allowed_children = lookml.lib.language_data._allowed_children._allowed_children
    config = lookml.lib.language_data.config.config
    click.echo(_allowed_children)

@click.command()
# @click.option('--repository',  prompt='repo i.e. llooker/mycompany',help='github repo containing the project')
@click.option('--access_token',  prompt='your github access token',help='github personal access token')
@click.option('--looker_host',  prompt='looker host https://demo.looker.com/',help='looker host to work upon')
@click.option('--api_client',  prompt='Client ID',help='Looker API client ID')
@click.option('--api_secret',  prompt='API Secret Key',help='Looker API Secret')
@click.option('--model_name',  prompt='Looker Model Name',help='model to evaluate, i.e. hr_analytics')
@click.option('--branch',  prompt='git branch',help='master by default, can be your dev branch')
def autotune(
        #  repository
         access_token
        ,looker_host
        ,api_client
        ,api_secret
        ,model_name
        ,branch
    ):
    click.echo(
        f'Welcome to autotune'
        # f'\nrepository: {repository}'
        f'\naccess_token: {access_token}'
        f'\nlooker_host: {looker_host}'
        f'\napi_client: {api_client}'
        f'\napi_secret: {api_secret}'
        f'\nmodel_name: {model_name}'
        f'\nbranch: {branch}'
        )
    os.environ['LOOKERSDK_BASE_URL'] = looker_host
    os.environ['LOOKERSDK_CLIENT_ID'] = api_client
    os.environ['LOOKERSDK_CLIENT_SECRET'] = api_secret
    os.environ['LOOKERSDK_VERIFY_SSL'] = 'true'
    os.environ['LOOKERSDK_TIMEOUT'] = '120'
    os.environ['LOOKERSDK_API_VERSION'] = '4.0'
    sdk = looker_sdk.init40()
    # foo = sdk.me()
    # click.echo(str(foo.email))
    # try:
        # sdk = looker_sdk.init40("tests/api.ini")
    frequent_queries = sdk.run_inline_query(result_format='json',body={
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
                "limit": "10"
            })
    click.echo(frequent_queries)
    frequent_queries = json.loads(frequent_queries)
    
    field_type_index = dict()
    for query in frequent_queries:
        #look up the model attributes
        model = sdk.lookml_model(query["query.model"])
        #look up the project attributes
        looker_project = sdk.project(model.project_name)
        if looker_project.git_service_name == 'github': #and looker_project.name == 'dbs':
            git_search = re.search(
                r'git@github.com:([a-zA-Z0-9_]{1,100}\/[a-zA-Z_0-9]{1,100})\.git', 
                looker_project.git_remote_url)
            if git_search:
                repo = git_search.group(1)
                click.echo(f'repo: {repo}')
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
            # try:
            #P0: better port handling, ask the user for the explicit host
            if looker_host.endswith(':19999'):
                looker_host = looker_host[:-6] + '/'
            pylookml_project = lookml.Project(
                repo= repo
                # ,access_token=config['project1']['access_token']
                ,access_token=access_token
                # ,looker_host='https://dat.dev.looker.com/'
                ,looker_host=looker_host
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
                }}'''
            fields = json.loads(query["query.formatted_fields"])
            for field in fields:
                if field in field_type_index[looker_project.name][query["query.model"]][query["query.view"]]["dimensions"]:
                    pylookml_explore.aggregate_table["auto_pylookml_"+query["query.slug"]].query.dimensions + field
                if field in field_type_index[looker_project.name][query["query.model"]][query["query.view"]]["measures"]:
                    pylookml_explore.aggregate_table["auto_pylookml_"+query["query.slug"]].query.measures + field
            filters = json.loads(query["query.filters"])
            #P1: aggregate tables can't take paramter fields. Need to ensure each filter is not a param
            pylookml_explore.aggregate_table["auto_pylookml_"+query["query.slug"]].query.filters + {k:v[1:][:-1] for k,v in filters.items()}
            pylookml_model.write()
            # pylookml_project.put(pylookml_model)
            #P1: put a https://dat.dev.looker.com/x/<<slug>> in the description
            # except:
            #     e = sys.exc_info()[0]
            #     click.echo(f'Unexpected error: {e}')
    # except:
    #     click.echo(f'error, review your inputs and try again {sys.exc_info()[0]}')

cli.add_command(doctree)
cli.add_command(autotune)
cli.add_command(directory)

if __name__ == '__main__':
    cli()