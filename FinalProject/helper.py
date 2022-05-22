import configparser
import getpass

import requests


def enum(**enums):
    return type('Enum', (), enums)


def gen_auth_cookie(enable=True):
    if not enable:
        return

    passwd = getpass.getpass('Password :: ')
    user = 'dlad-account'

    config = configparser.ConfigParser()
    config.read('config.ini')

    url_to_get_cookie = config['ipam']['networkview']
    response = requests.get(url_to_get_cookie, auth=(user, passwd), verify=False)
    authcookie = response.cookies['ibapauth']

    request_cookies = {'ibapauth': authcookie}  # set the cookie to a varibale
    return request_cookies
