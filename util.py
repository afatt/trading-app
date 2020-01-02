#!/usr/bin/python
'''
'''

import yaml

def load_login_info():
    with open('user_pass.yml') as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        username = user_pass['username']
        password = user_pass['password']
    return [username, password]
