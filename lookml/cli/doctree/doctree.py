import click
import lookml
import pprint

@click.command()
def doctree():
    '''
    Lists the parameter tree of LookML and links to documentation
    '''
    _allowed_children = lookml.lib.language_data._allowed_children._allowed_children
    config = lookml.lib.language_data.config.config
    click.echo(pprint.pprint(_allowed_children))