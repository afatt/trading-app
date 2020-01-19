#!/usr/bin/env python
'''Check user_info.yml and create if doesnt exist
   Prompt the user for robinhood username and password and save in user_info.yml
   Prompt user for day of the week Monday - Friday to automatically invest
   Prompt the user for contribution amount in $ (US Dollars)
   Run trader.py
'''
# Standard Library
import time
from os import path

# Third Party
import schedule

# Local Modules
import trader
import util
import robinhood_wrapper as broker

FILE_NAME = 'user_info.yml'

def check_user_info():
    '''Check for user_info.yml and create if it doesn't exist
    '''
    if not path.exists(FILE_NAME):
        print('File doesnt exist')
        util.build_yaml()
        return True
    else:
        print('User info found')
        user_info = util.get_user_info()
        print('-----------------------------------------------------')
        print('Username:        %s' % user_info['username'])
        print('Password:        %s' % user_info['password'])
        print('Investment Day: %s' % user_info['day_of_week'])
        print('Investment time: %s' % user_info['time_of_day'])
        print('Contribution:    $%s' % str(user_info['contribution']))
        print('-----------------------------------------------------')
        while True:
            yes_no = input('Would you like to change any settings? (y/n): ')
            if 'y' in yes_no.lower():
                return True
            elif 'n' in yes_no.lower():
                return False
            else:
                print('Please type yes or no, try again')

def prompt_user_pass():
    '''Prompt the user for robinhood username and password and save in
       user_info.yml
    '''
    username = input('Enter your Robinhood username/email: ')
    password = input('Enter your Robinhood password: ')
    util.set_param('username', username)
    util.set_param('password', password)

def prompt_day_of_week():
    '''Prompt user for day of the week Monday - Friday to automatically invest
    '''
    print('                 Options')
    print('--------------------------------------------')
    print('Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday')
    day_of_week = input('Enter the day or days of the week you '
                        'would like to invest: ')
    day_of_week = day_of_week.lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday',
            'friday', 'saturday', 'sunday']
    set_day = ''
    for day in days:
        if day in day_of_week:
            set_day += ' ' + day
    util.set_param('day_of_week', set_day)

def prompt_contribution():
    '''Prompt the user for contribution amount in $ (US Dollars)
    '''
    contribution = input('Enter the amount you would like to invest: ')
    contribution = float(contribution)
    util.set_param('contribution', contribution)

def prompt_time_of_day():
    '''Prompt the user to set time of the day to run the trader
    '''
    time_of_day = input('Enter the time of day to run (Ex. 15:30): ')
    util.set_param('time_of_day', time_of_day)

def execute_trader():
    '''
    '''
    print('Trader Started!')
    # If portfolio hits the 52 dividend stocks quota start balancing model
    dividend_analyzer = trader.DividendAnalyzer()
    trader_dividend = trader.Trader(dividend_analyzer)

    day_of_week = util.get_day_of_week()
    time_of_day = util.get_time_of_day()
    if 'monday' in day_of_week:
        print('Executing trader at %s on Monday' % time_of_day)
        schedule.every().monday.at(time_of_day).do(trader_dividend.execute_model)
    if 'tuesday' in day_of_week:
        print('Executing trader at %s on Tuesday' % time_of_day)
        schedule.every().tuesday.at(time_of_day).do(trader_dividend.execute_model)
    if 'wednesday' in day_of_week:
        print('Executing trader at %s on Wednesday' % time_of_day)
        schedule.every().wednesday.at(time_of_day).do(trader_dividend.execute_model)
    if 'thursday' in day_of_week:
        print('Executing trader at %s on Thursday' % time_of_day)
        schedule.every().thursday.at(time_of_day).do(trader_dividend.execute_model)
    if 'friday' in day_of_week:
        print('Executing trader at %s on Friday' % time_of_day)
        schedule.every().friday.at(time_of_day).do(trader_dividend.execute_model)
    if 'saturday' in day_of_week:
        print('Executing trader at %s on Saturday' % time_of_day)
        print('Order will be placed however, purchase will execute on the next '
              'open trading day')
        schedule.every().saturday.at(time_of_day).do(trader_dividend.execute_model)
    if 'sunday' in day_of_week:
        print('Executing trader at %s on Sunday' % time_of_day)
        print('Order will be placed however, purchase will execute on the next '
              'open trading day')
        schedule.every().sunday.at(time_of_day).do(trader_dividend.execute_model)

    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    if check_user_info():
        prompt_user_pass()
        prompt_day_of_week()
        prompt_contribution()
        prompt_time_of_day()
    execute_trader()

if __name__ == '__main__':
    main()
