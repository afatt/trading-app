#!/usr/bin/env python
'''The main in this module is for testing new functions and changes only
'''

import util
import pymysql
import robin_stocks
from io import StringIO

def robinhood_auth(usr, pwd, exp, scope, sms, store_session):
    '''Authorization to robinhood account:
       Required Params: usr = (str) username, pwd = (str) password,
       Optional Params: exp = (int) seconds till session expires,
                        scope = (str) scope of authentication,
                        sms = (boolean) email(False) or sms(True),
                        store_session = whether to save the login
                        authorization for future logins
               Returns: dictionary with keys 'access_token' and 'detail'
    '''
    # Send message to app.js saying to input mfa_code

    token_dict = robin_stocks.login(usr, pwd, exp, scope, sms, store_session)
    return token_dict

def market_buy(symbol, quantity, time):
    order_info = robin_stocks.order_buy_market(symbol, quantity, time)
    return order_info

def get_hist_price(symbol, span, bounds):
    try:
        hist_data = robin_stocks.get_historicals(symbol, span, bounds)
    except Exception as err:
        print(err)
    return hist_data

def get_latest_pricing(symbol):
    price = robin_stocks.get_latest_price(symbol)[0]
    price = float(price)
    return price

def get_portfolio():
    symbols = []
    my_stocks = robin_stocks.build_holdings()
    for key, value in my_stocks.items():
        symbols.append(key)
    return symbols

def cancel_orders():
    try:
        canceled_orders = robin_stocks.cancel_all_open_orders()
    except Exception:
        pass
    return canceled_orders

def get_cash():
    cash = robin_stocks.load_account_profile()['cash']
    cash = float(cash)
    return cash

def get_equity():
    equity = robin_stocks.build_user_profile()['equity']
    equity = float(equity)
    return equity

def get_buying_power():
    buying_power = robin_stocks.load_account_profile()['buying_power']
    buying_power = float(buying_power)
    return buying_power

def get_watchlist_symbols():
    '''Returns the watchlist symbols from the user's Robinhood account
       Symbols from user's portfolio will be removed to avoid repurchase
       Symbols with broken url will not be added to the list
    '''
    watchlist_symbols = []
    try:
        instrument_dict = robin_stocks.get_watchlist_by_name('Default')
    except Exception:
        raise Exception('Could not return Default Watchlist')
    #print(instrument_dict)

    instrument_data = [robin_stocks.get_instrument_by_url(item['instrument']) \
                       for item in instrument_dict if item]
    watchlist_symbols = [item['symbol'] for item in instrument_data if item]

    # Remove stocks in your portfolio from the watchlist
    portfolio = get_portfolio()
    for symbol in list(watchlist_symbols):
        if symbol in portfolio:
            watchlist_symbols.remove(symbol)
    return watchlist_symbols

def post_watchlist(symbols):
    try:
        robin_stocks.post_symbols_to_watchlist(symbols)
    except Exception:
        pass

def get_open_orders():
    open_orders = robin_stocks.get_all_open_orders()
    if open_orders[0] is None:
        return False
    else:
        return open_orders

def get_order_state():
    open_orders = robin_stocks.get_all_open_orders()
    if open_orders[0] is None:
        return False
    else:
        state = open_orders[0]['state']
        return state

def get_dividend_yield(symbol):
    fundamentals = robin_stocks.get_fundamentals(symbol)
    dividend_yield = fundamentals[0]['dividend_yield']
    dividend_yield = float(dividend_yield)
    return dividend_yield

def get_dividend(symbol):
    dividend_yield = get_dividend_yield(symbol)
    current_price = get_latest_pricing(symbol)
    dividend = round(current_price * (dividend_yield / 100), 2)
    return dividend

def get_payout_ratio(symbol):
    # payout_ratio = dividend / current_eps_estimate
    eps_estimate = get_eps_estimates(symbol)[-1:]
    payout_ratio = (get_dividend(symbol) / 4.0 / eps_estimate[0]) * 100
    payout_ratio = round(payout_ratio, 2)
    return payout_ratio

def get_price_earnings_ratio(symbol):
    fundamentals = robin_stocks.get_fundamentals(symbol)
    pe_ratio = fundamentals[0]['pe_ratio']
    return pe_ratio

def get_buy_rating(symbol):
    rating_info = robin_stocks.get_ratings(symbol)
    if rating_info['summary'] is None:
        return None
    else:
        rating_summary = rating_info['summary']
        buy_rating = rating_summary['num_buy_ratings']
        buy_rating = float(buy_rating)
        return buy_rating

def get_sell_rating(symbol):
    rating_info = robin_stocks.get_ratings(symbol)
    if rating_info['summary'] is None:
        return None
    else:
        rating_summary = rating_info['summary']
        sell_rating = rating_summary['num_sell_ratings']
        sell_rating = float(sell_rating)
        return sell_rating

def get_hold_rating(symbol):
    rating_info = robin_stocks.get_ratings(symbol)
    if rating_info['summary'] is None:
        return None
    else:
        rating_summary = rating_info['summary']
        hold_rating = rating_summary['num_hold_ratings']
        hold_rating = float(hold_rating)
        return hold_rating

def get_eps_actuals(symbol):
    eps = []
    eps_actuals = []
    eps_info = robin_stocks.get_earnings(symbol)

    # Some companies do not provide EPS data
    if eps_info[0] is None:
        return None
    else:
        eps = [item['eps'] for item in eps_info]
        eps_actuals = [item['actual'] for item in eps]
        eps_actuals = [float(i) for i in eps_actuals if i is not None]
        return eps_actuals

def get_eps_estimates(symbol):
    eps = []
    eps_estimates = []
    eps_info = robin_stocks.get_earnings(symbol)

    # Some companies do not provide EPS data
    if eps_info[0] is None:
        return None
    else:
        eps = [item['eps'] for item in eps_info]
        eps_estimates = [item['estimate'] for item in eps]
        eps_estimates = [float(i) for i in eps_estimates if i is not None]
        return eps_estimates

def get_shares_outstanding(symbol):
    fundamentals = robin_stocks.get_fundamentals(symbol)
    shares_outstanding = fundamentals[0]['shares_outstanding']
    shares_outstanding = float(shares_outstanding)
    return shares_outstanding

def get_net_income(symbol):
    eps_actuals = get_eps_actuals(symbol)
    print(eps_actuals)
    eps_latest = eps_actuals[-2:]
    eps_latest = eps_latest[0]
    print(eps_latest)
    shares_outstanding = get_shares_outstanding(symbol)
    net_income = eps_latest * shares_outstanding #+ preferred_dividends
    return net_income


def main():
    # FOR TESTING PURPOSES ONLY
    username, password = util.get_login_info()
    token_dict = robinhood_auth(username, password , 86400 * 7,
                                'internal', True, True )
    url = 'https://api.robinhood.com/oauth2/token'
    payload = {
        'client_id': 'c82SH0WZOsabOXGP2sxqcj34FxkvfnWRZBKlBjFS',
        'expires_in': 86400,
        'grant_type': 'password',
        'password': 'THISismylogin@87',
        'scope': 'internal',
        'username': 'afatt90@gmail.com',
        'challenge_type': 'sms',
        'device_token': '86188087-ade1-0522-8600-a06d45b7b8be'
        }
    res = robin_stocks.helper.request_post(url, payload)
    print(res)

if __name__ == '__main__':
    main()
