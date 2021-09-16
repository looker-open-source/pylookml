import lookml
import click
import os
from looker_sdk import models, methods, init40
import json, re, sys, pkg_resources
import pprint
from .cli.autotune.autotune import autotune as autotune
from .cli.doctree.doctree import doctree as doctree
from .cli.directory.directory import directory as directory
import configparser
from pathlib import Path
import github
import shutil
from lookml.lib import utils

#P3 CLI show children report for a specific field
#P3 CLI change a dimension name safely
#P3 CLI create LookML from a well known artifact from another tool
#P3 CLI apply block
#P3 CLI auto-tune your Looker Instance (create aggregate tables for top queries)
# write logs to a file in cwd
#P3 CLI add sums & averages of all number dimensions 




@click.group()
@click.option('--config', envvar='CONFIG')
@click.pass_context
def cli(ctx, config):
    ctx.obj = utils.Conf(config)

@click.command()
def version():
    '''Provides currently installed PyLookML Version'''
    click.echo(pkg_resources.get_distribution('lookml').version)

@click.command()
@click.option('--use')
@click.option('--looker_project_name')
@click.option('--github_repo_name')
@click.pass_obj
def push(ctx,use, looker_project_name, github_repo_name):
    # print(ctx.conf[use]['base_url'])
    # connect to Looker
    os.environ['LOOKERSDK_BASE_URL'] = ctx.conf[use]['base_url']
    os.environ['LOOKERSDK_CLIENT_ID'] =  ctx.conf[use]['client_id']
    os.environ['LOOKERSDK_CLIENT_SECRET'] =  ctx.conf[use]['client_secret']
    sdk = init40()
    sdk.update_session(body={ 'workspace_id': 'dev'})
    # connect to github
    _github = github.Github(ctx.conf[use]['access_token'])
    # create repo on github
    user = _github.get_user()
    repo = user.create_repo(github_repo_name)
    # repo = user.get_repo('example_789')
    p = sdk.create_project({
            "id": looker_project_name,
            "name": looker_project_name,
            "uses_git": True,
            # "git_remote_url": repo.ssh_url,
            # "git_username": "string",
            # "git_password": "string",
            # "git_username_user_attribute": "string",
            # "git_password_user_attribute": "string",
            # "git_service_name": "string",
            # "git_application_server_http_port": 0,
            # "git_application_server_http_scheme": "string",
            # "deploy_secret": "string",
            # "unset_deploy_secret": true,
            # "pull_request_mode": "string",
            # "validation_required": true,
            # "git_release_mgmt_enabled": true,
            # "allow_warnings": true,
            # "is_example": true,
            # "dependency_status": "string"
        })
    deploy_key = sdk.create_git_deploy_key(p.id)
    sdk.update_project(looker_project_name, {"git_remote_url": repo.ssh_url})
    repo.create_key(title='looker_deploy_key_pylookml',key=deploy_key)

@click.command()
@click.argument('name')
def init(name):
    os.makedirs(f'{name}')

@click.command()
@click.argument('name')
def new(name):
    proj = lookml.Project(path='.')
    f = proj.new_file(name)
    f.write()

@click.command()
@click.argument('name')
@click.argument('file')
def view(name, file):
    proj = lookml.Project(path='.')
    f = proj.file(file)
    f + lookml.View(f'view: {name} {{}}')
    f.write()

@click.command()
@click.option('--use')
@click.option('--github_repo_name')
@click.pass_obj
def origin(ctx,use, github_repo_name):
    proj_local = lookml.Project(path='.')
    proj_remote = lookml.ProjectGithub(
        repo=github_repo_name,
        access_token=ctx.conf[use]['access_token']
    )
    print(proj_remote._git_connection)
    for f in proj_local.files():
        proj_remote.new_file(f.path)
        f2 = proj_remote[f.path]
        for v in f['views']:
            f2 + str(v)
        f2.write()

@click.command()
@click.option('--use')
@click.option('--github_repo_name')
@click.pass_obj
def clone(ctx,use, github_repo_name):
    looker_project_name = github_repo_name
    x = lookml.ProjectSSH(path='.',git_url='git@github.com:llooker/SFDC_campaign_attribution.git',looker_project_name=looker_project_name)
    shutil.rmtree(f'./{x._looker_project_name}/.git')
    os.environ['LOOKERSDK_BASE_URL'] = ctx.conf[use]['base_url']
    os.environ['LOOKERSDK_CLIENT_ID'] =  ctx.conf[use]['client_id']
    os.environ['LOOKERSDK_CLIENT_SECRET'] =  ctx.conf[use]['client_secret']
    sdk = init40()
    sdk.update_session(body={ 'workspace_id': 'dev'})
    # connect to github
    _github = github.Github(ctx.conf[use]['access_token'])
    # create repo on github
    user = _github.get_user()
    repo = user.create_repo(github_repo_name)
    # repo = user.get_repo('example_789')
    p = sdk.create_project({
            "id": looker_project_name,
            "name": looker_project_name,
            "uses_git": True,
            # "git_remote_url": repo.ssh_url,
            # "git_username": "string",
            # "git_password": "string",
            # "git_username_user_attribute": "string",
            # "git_password_user_attribute": "string",
            # "git_service_name": "string",
            # "git_application_server_http_port": 0,
            # "git_application_server_http_scheme": "string",
            # "deploy_secret": "string",
            # "unset_deploy_secret": true,
            # "pull_request_mode": "string",
            # "validation_required": true,
            # "git_release_mgmt_enabled": true,
            # "allow_warnings": true,
            # "is_example": true,
            # "dependency_status": "string"
        })
    deploy_key = sdk.create_git_deploy_key(p.id)
    sdk.update_project(looker_project_name, {"git_remote_url": repo.ssh_url})
    repo.create_key(title='looker_deploy_key_pylookml',key=deploy_key)
    shutil.move(looker_project_name,looker_project_name+'_')
    y = lookml.ProjectSSH(path='.',git_url=repo.ssh_url,looker_project_name=looker_project_name)
    shutil.copytree(looker_project_name+'_/',looker_project_name+'/', dirs_exist_ok=True)
    y._git.add()
    y._git.push_origin_head()
    # y.commit()
    shutil.rmtree(looker_project_name+'_')



cli.add_command(doctree)
cli.add_command(autotune)
cli.add_command(directory)
cli.add_command(version)
cli.add_command(push)
cli.add_command(init)
cli.add_command(new)
cli.add_command(view)
cli.add_command(origin)
cli.add_command(clone)

if __name__ == '__main__':
    cli()