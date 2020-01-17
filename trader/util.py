#!/usr/bin/env python
'''
'''

import yaml

FILE_NAME = 'user_info.yml'

def build_yaml():
    info_dict = {'username': 'username',
                 'password': 'password',
                 'contribution': 0.0,
                 'day_of_week': 'monday',
                 'time_of_day': '10:00'}
    with open(FILE_NAME, 'w') as file:
        info = yaml.dump(info_dict, file)

def get_contribution():
    with open(FILE_NAME) as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        contribution = user_pass['contribution']
    return contribution

def get_day_of_week():
    with open(FILE_NAME) as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        contribution = user_pass['day_of_week']
    return contribution

def get_login_info():
    with open(FILE_NAME) as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        username = user_pass['username']
        password = user_pass['password']
    return [username, password]

def get_time_of_day():
    with open(FILE_NAME) as file:
        user_pass = yaml.load(file, Loader=yaml.FullLoader)
        contribution = user_pass['time_of_day']
    return contribution

def get_user_info():
    with open(FILE_NAME) as file:
        info_dict = yaml.load(file, Loader=yaml.FullLoader)
    return info_dict

def set_param(key_name, value):
    with open(FILE_NAME) as file:
        info_dict = yaml.load(file, Loader=yaml.FullLoader)
        info_dict[key_name] = value

    with open(FILE_NAME, 'w') as file:
        info = yaml.dump(info_dict, file)
