#!/usr/bin/python
'''The main in this module is for testing new functions and changes only
'''

import yfinance as yf

def get_info(symbol):
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    return stock_info

def get_payout_ratio(symbol):
    stock = yf.Ticker(symbol)
    payout_ratio = stock.info['payoutRatio']
    if payout_ratio is None: #Raises TypeError
        return None
    else:
        payout_ratio = round(payout_ratio * 100, 2)
        return payout_ratio

def get_dividend(symbol):
    stock = yf.Ticker(symbol)
    dividend = stock.info['dividendRate']
    dividend = float(dividend)
    return dividend

def get_industry(symbol):
    stock = yf.Ticker(symbol)
    industry = stock.info['industry']
    return industry

def get_sector(symbol):
    stock = yf.Ticker(symbol)
    sector = stock.info['sector']
    return sector

def get_forward_eps(symbol):
    stock = yf.Ticker(symbol)
    forward_eps = stock.info['forwardEps']
    forward_eps = float(forward_eps)
    return forward_eps

def main():
    # FOR TESTING PURPOSES ONLY
    symbol = 'MED'
    print(get_sector(symbol))

if __name__ == '__main__':
    main()
