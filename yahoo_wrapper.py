#!/usr/bin/python
'''
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

def get_test(symbol):
    stock = yf.Ticker(symbol)
    est = stock.quarterly_earnings
    return est

def get_cashflow(symbol):
    stock = yf.Ticker(symbol)
    est = stock.financials
    return est

def get_trailing_eps(symbol):
    stock = yf.Ticker(symbol)
    trailing_eps = stock.info['trailingEps']
    trailing_eps = float(trailing_eps)
    return trailing_eps

def main():
    # FOR TESTING PURPOSES ONLY
    symbol = 'MED'
    print(get_info(symbol))
    print(get_payout_ratio(symbol))
    print(get_trailing_eps(symbol))

if __name__ == '__main__':
    main()
