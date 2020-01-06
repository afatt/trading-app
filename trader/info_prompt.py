#!/usr/bin/python
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
    else:
        print('User info found')
        user_info = util.get_user_info()
        print('-----------------------------------------------------')
        print('Username:        %s' % user_info['username'])
        print('Password:        %s' % user_info['password'])
        print('Investment Day:  %s' % user_info['day_of_week'])
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

def execute_trader():
    '''
    '''
    print('Trader Started!')
    # If portfolio hits the 52 dividend stocks quota start balancing model
    dividend_analyzer = trader.DividendAnalyzer()
    trader_dividend = trader.Trader(dividend_analyzer)

    day_of_week = util.get_day_of_week()
    day_of_week = day_of_week.lower()
    if day_of_week in 'monday':
        print('Executing trader at 10:00am on Monday')
        schedule.every().monday.at('16:04').do(trader_dividend.execute_model)
    elif day_of_week in 'tuesday':
        schedule.every().tuesday.at('10:00').do(trader_dividend.execute_model)
    elif day_of_week in 'wednesday':
        schedule.every().wednesday.at('10:00').do(trader_dividend.execute_model)
    elif day_of_week in 'thursday':
        schedule.every().thursday.at('10:00').do(trader_dividend.execute_model)
    else:
        schedule.every().friday.at('10:00').do(trader_dividend.execute_model)

    #schedule.every(1).minutes.do(trader_dividend.execute_model)
    #schedule.every(1).saturday.at('15:56').do(trader_dividend.execute_model)
    while True:
        schedule.run_pending()
        time.sleep(1)

def main():
    if check_user_info():
        prompt_user_pass()
        prompt_day_of_week()
        prompt_contribution()
    execute_trader()

if __name__ == '__main__':
    main()