#!/usr/bin/python
'''Check user_info.yml and create if doesnt exist
   Prompt the user for robinhood username and password and save in user_info.yml
   Prompt user for day of the week Monday - Friday to automatically invest
   Prompt the user for contribution amount in $ (US Dollars)
   Run trader.py
'''

from os import path

def check_user_info():
    '''Check for user_info.yml and create if it doesn't exist
    '''
    if not path.exists('user_info.yml'):
        print('File doesnt exist')
    else:
        print('File does exist')

def prompt_user_pass():
    '''Prompt the user for robinhood username and password and save in
       user_info.yml
    '''

def prompt_day_of_week():
    '''Prompt user for day of the week Monday - Friday to automatically invest
    '''

def prompt_contribution():
    '''Prompt the user for contribution amount in $ (US Dollars)
    '''

def main():
    check_user_info()

if __name__ == '__main__':
    main()
