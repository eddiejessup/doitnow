#!/usr/bin/env python3

import logging
from os.path import join, expanduser
from pprint import pprint as pp

import click
import todoist

import utils


DEFAULT_CACHE_PATH = expanduser('~/.todoist-cache')
DEFAULT_CONFIG_PATH = expanduser('~/.doitrc')


def get_project_by_name(api, name):
    results = [r for r in api.state['projects'] if r['name'] == name]
    if len(results) > 1:
        raise ValueError('Multiple projects with this name')
    return results[0]


@click.group()
def doit():
    pass


# Note: method on `doit`, not `click`, to attach sub-command.
@doit.command()
@click.argument('content')
@click.option('--time', default='',
              help='Task time.')
@click.option('--project',
              help='Project to add task to.')
@click.option('--email',
              help='The email address of the account.')
@click.option('--config_path', default=DEFAULT_CONFIG_PATH,
              help='Path to the doitnow configuration file, if any.')
@click.option('--fresh', is_flag=True,
              help='Start a new session even if cache exists.')
@click.option('--debug', is_flag=True,
              help='Enable logging')
def add(content, time, project, email, config_path, fresh, debug):
    """Log in to Todoist account."""
    if debug:
        logging.basicConfig(level=logging.INFO)

    api = utils.get_api(email, config_path, fresh)
    if project is not None:
        project_obj = get_project_by_name(api, project)
        import pdb; pdb.set_trace()
    else:
        project_id = None
    api.items.add(content, project_id, date_string=time)
    api.commit()
if __name__ == '__main__':
    doit()
