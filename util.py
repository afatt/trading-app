#!/usr/bin/python
'''
'''

import yaml

def get_login_info():
    with open('user_info.yml') as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        username = user_pass['username']
        password = user_pass['password']
    return [username, password]

def get_contribution():
    with open('user_info.yml') as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        contribution = user_pass['contribution']
    return contribution
