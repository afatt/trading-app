#!/usr/bin/python
'''Check user_info.yml and create if doesnt exist
   Prompt the user for robinhood username and password and save in user_info.yml
   Prompt user for day of the week Monday - Friday to automatically invest
   Prompt the user for contribution amount in $ (US Dollars)
   Run trader.py
'''

from os import path

import util
import robinhood_wrapper as broker

FILE_NAME = 'user_info.yml'

def check_user_info():
    '''Check for user_info.yml and create if it doesn't exist
    '''
    if not path.exists(FILE_NAME):
        print('File doesnt exist')
        util.build_yaml()
    else:
        print('File does exist')
        print('User info printed here')
        print('Would you like to change any settings?')

def prompt_user_pass():
    '''Prompt the user for robinhood username and password and save in
       user_info.yml
    '''
    username = input('Enter your Robinhood username: ')
    password = input('Enter your Robinhood password: ')
    util.set_param('username', username)
    util.set_param('password', password)

def prompt_day_of_week():
    '''Prompt user for day of the week Monday - Friday to automatically invest
    '''
    print('                 Options')
    print('--------------------------------------------')
    print('Monday, Tuesday, Wednesday, Thursday, Friday')
    day_of_week = input('Enter the day of the week you would like to invest: ')
    if day_of_week.lower() in 'monday tuesday wednesday thursday friday':
        util.set_param('day_of_week', day_of_week)
    else:
        print('Day of week not found, try again')

def prompt_contribution():
    '''Prompt the user for contribution amount in $ (US Dollars)
    '''
    contribution = input('Enter the amount you would like to invest each week: ')
    contribution = float(contribution)
    util.set_param('contribution', contribution)

def main():
    check_user_info()
    prompt_user_pass()
    prompt_day_of_week()
    prompt_contribution()

if __name__ == '__main__':
    main()
