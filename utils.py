import logging
from os.path import join, expanduser
from configparser import ConfigParser
import getpass

import todoist

logger = logging.getLogger(__name__)


def get_api(email, config_path, fresh):
    config = ConfigParser()
    logger.info('Reading config file {}'.format(config_path))
    config.read(config_path)

    logger.debug('Config contents:')
    for key in config:
        logger.debug(config[key])

    if email is None:
        if config.has_option('auth', 'email'):
            email = config['auth']['email']
            logger.info('Read email from config file: {}'.format(email))
        else:
            email = input('Email address: ')

    if fresh:
        token = None
        logger.info('Fresh flag setting initial token to {}'.format(token))
    elif 'session' in config:
        token = config['session'].get('token')
        logger.info('Read token from config file: {}'.format(token))
    else:
        token = None
        logger.info('No token found in config file')

    logger.info('Initializing API object with token: {}'.format(token))
    api = todoist.TodoistAPI(token=token)

    if api.token is None:
        logger.info('No initial token for API, logging in')
        if config.has_option('auth', 'password'):
            password = config['auth']['password']
            logger.info('Read password from config file')
        else:
            password = getpass.getpass(prompt='Password: ')

        user = api.user.login(email, password)
        success = ('error' not in user) and (api.token is not None)
        logger.info('Attempted login, status: {}'.format(success))
        logger.debug('Login response: {}'.format(user))
        if success:
            logger.info('Setting session token in config to {}'
                        .format(api.token))
            if 'session' not in config:
                logger.info('Creating session section in config file')
                config['session'] = {}
            config['session']['token'] = api.token
            logger.info('Writing to config file: {}'.format(config_path))
            with open(config_path, 'w') as config_file:
                config.write(config_file)
        else:
            raise ValueError
    return api
