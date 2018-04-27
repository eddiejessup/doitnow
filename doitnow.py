#!/usr/bin/env python3

import logging
from os.path import join, expanduser
from pprint import pprint as pp

import click
import todoist

import utils


DEFAULT_CACHE_PATH = expanduser('~/.todoist-cache')
DEFAULT_CONFIG_PATH = expanduser('~/.doitrc')


@click.group()
@click.option('--email',
              help='The email address of the account.')
@click.option('--config_path', default=DEFAULT_CONFIG_PATH,
              type=click.Path(resolve_path=True),
              help='Path to the doitnow configuration file, if any.')
@click.option('--fresh/--no-fresh',
              help='Start a new session even if cache exists.')
@click.option('--debug/--no-debug',
              help='Enable logging')
@click.pass_context
def doit(ctx, email, config_path, fresh, debug):
    if debug:
        logging.basicConfig(level=logging.INFO)
    api = utils.get_api(email, config_path, fresh)
    ctx.obj['api'] = api



# Note: method on `doit`, not `click`, to attach sub-command.
@doit.command()
@click.argument('content')
@click.option('-t', '--time', default='',
              help='Task time.')
@click.option('-p', '--project',
              help='Project to add task to.')
@click.pass_context
def add(ctx, content, time, project):
    """Add a task."""
    api = ctx.obj['api']
    if project is not None:
        project_obj = utils.get_project_by_name(api, project)
        project_id = project_obj['id']
    else:
        project_id = None
    api.items.add(content, project_id, date_string=time)
    api.commit()


if __name__ == '__main__':
    doit(obj={})
