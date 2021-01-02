#from lookml import core as lookml
import lookml
import click
import os
import looker_sdk
import json, re, sys, pkg_resources
import pprint
from .cli.autotune.autotune import autotune as autotune
from .cli.doctree.doctree import doctree as doctree
from .cli.directory.directory import directory as directory

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
def version():
    '''Provides currently installed PyLookML Version'''
    click.echo(pkg_resources.get_distribution('lookml').version)


cli.add_command(doctree)
cli.add_command(autotune)
cli.add_command(directory)
cli.add_command(version)

if __name__ == '__main__':
    cli()