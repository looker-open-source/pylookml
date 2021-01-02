import click
import lookml
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