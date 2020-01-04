#!/usr/bin/python
'''
'''

# Standard Library
import abc
import time
import logging
from datetime import datetime

# Third Party
import schedule

# Local Modules
import util
import robinhood_wrapper as broker
import yahoo_wrapper as yahoo


class Trader():

    def __init__(self, model):
        self._model = model
        self._username, self._password = util.get_login_info()
        self._token_dict = broker.robinhood_auth(self._username,
                                                 self._password, 86400,
                                                 'internal', True, True )

    def execute_model(self):
        self._model.model_interface()


class Model(abc.ABC):
    '''Strategy that allows the Trader to implement different types of models
       Types: Volume, Moving Average, Exponential Moving Average, Relative
       Strength Index, Moving Average Convergence Divergence, Dividends
    '''

    @abc.abstractmethod
    def model_interface(self):
        pass


class DividendAnalyzer(Model):

    def __init__(self):
        logging.basicConfig(filename='dividend_analyzer.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%H:%M:%S')

    def model_interface(self):
        start_time = datetime.now()
        prospects = broker.get_watchlist_symbols()
        purchase_symbol = self.trade_study(prospects)
        num_shares = self.order_quantity(purchase_symbol)
        # Make this its own method
        # Check if the buying_power is enough to purchase this many stocks
        # possibly a return item from order_quantity()
        #order_info = broker.market_buy(purchase_symbol, num_shares, time='gfd')
        #print(order_info)
        print('Purchasing %s shares of %s' % (str(num_shares), purchase_symbol))
        print('Ran in %s seconds' % str(datetime.now() - start_time))
        #logging.INFO('Purchasing %s shares of %s' % (str(num_shares), purchase_symbol))

    def trade_study(self, prospects):
        '''Why certain weights got the value they did
           returns: Stock symbol with the highest score
        '''

        # Weights on a scale of 1 to 5
        # Place into a yaml file and let advanced users tweak the weights
        eps_weight = 4.0
        payout_ratio_weight = 3.0
        annual_return_weight = 5.0
        analyst_rating_weight = 2.0
        #sector_weight = 2.0
        #fair_value_weight = 2.0

        # Dictionary to hold the total scores of each prospect
        # Symbol(key),  weighted_score(value)
        score_dict = {}

        for symbol in prospects:
            eps_score = self.eps_analysis(symbol)
            analyst_rating_score = self.analyst_rating_analysis(symbol)
            annual_return_score = self.annual_return_analysis(symbol)
            payout_ratio_score = self.payout_ratio_analysis(symbol)
            print(symbol)
            print('Eps: %s, ARating: %s, AnReturn: %s, PayRatio:'
                  ' %s' % (str(eps_score), str(analyst_rating_score), \
                  str(annual_return_score), str(payout_ratio_score)))
            unweighted_score = eps_score + analyst_rating_score + \
                               annual_return_score + payout_ratio_score
            weighted_score = eps_score * eps_weight + analyst_rating_score * \
                             analyst_rating_weight + annual_return_score * \
                             annual_return_weight + payout_ratio_score * \
                             payout_ratio_weight
            score_dict[symbol] = weighted_score
            # IF A SCORE IS TOO LOW REMOVE IT FROM THE WATCHLIST

        # Arange the dictionary from Highest Score to Lowest Score
        ranking_list = sorted(score_dict, key=score_dict.get, reverse=True)
        return ranking_list[0]

    def payout_ratio_analysis(self, symbol):
        '''Yahoo payout ratio is occasionally much greater than 100%. Need to
           find out how they do their calculation
        '''
        # payout_ratio = annual_dividend / curr_eps_estimated
        payout_ratio = yahoo.get_payout_ratio(symbol)
        if payout_ratio is None:
            payout_ratio_score = 1.0
            return payout_ratio_score
        else:
            if payout_ratio <= 20.0:
                payout_ratio_score = 5.0
            elif 30.0 >= payout_ratio > 20.0:
                payout_ratio_score = 4.0
            elif 40.0 >= payout_ratio > 30.0:
                payout_ratio_score = 3.0
            elif 50.0 >= payout_ratio > 40.0:
                payout_ratio_score = 2.0
            else:
                payout_ratio_score = 1.0
            return payout_ratio_score

    def annual_return_analysis(self, symbol):
        '''Calculates the annual return in dividends based on the user's weekly
           contribution and returns a score based of return thresholds
           returns: annual_return_score(float)
        '''
        dividend = broker.get_dividend(symbol)
        num_of_shares = self.order_quantity(symbol)
        annual_return = round(dividend * num_of_shares, 2)
        if annual_return > 20.0:
            annual_return_score = 5.0
        elif 15.0 < annual_return <= 20.0:
            annual_return_score = 4.0
        elif 10.0 < annual_return <= 15.0:
            annual_return_score = 3.0
        elif 5.0 < annual_return <= 10.0:
            annual_return_score = 2.0
        else:
            annual_return_score = 1.0
        return annual_return_score

    def order_quantity(self, symbol):
        '''Calculates the number of shares that can be ordered based off the
           user's weekly contribution
           returns: shares(int)
        '''
        contribution = util.get_contribution()
        current_price = broker.get_latest_pricing(symbol)
        shares = int(contribution / current_price)
        return shares

    def analyst_rating_analysis(self, symbol):
        '''
        '''
        num_buy_ratings = broker.get_buy_rating(symbol)
        if num_buy_ratings is None:
            analyst_score = 0.0
            return analyst_score
        else:
            num_sell_ratings = broker.get_sell_rating(symbol)
            num_hold_ratings = broker.get_hold_rating(symbol)
            num_ratings = num_buy_ratings + num_sell_ratings + num_hold_ratings
            buy_percent = round(num_buy_ratings / num_ratings * 100, 2)
            if buy_percent > 90.0:
                analyst_score = 5.0
            elif 80.0 < buy_percent <= 90.0:
                analyst_score = 4.0
            elif 70.0 < buy_percent <= 80.0:
                analyst_score = 3.0
            elif 60.0 < buy_percent <= 70.0:
                analyst_score = 2.0
            else:
                analyst_score = 1.0
            return analyst_score

    def eps_analysis(self, symbol):
        '''EPS (Earnings Per Share) Analysis
           Possibly include the trailing eps of the last 4 eps values
        '''
        eps_actuals = broker.get_eps_actuals(symbol)
        if eps_actuals is None:
            eps_score = 0.0
            return eps_score
        else:
            eps_average = self.simple_average(eps_actuals)
            eps_latest = eps_actuals[-2:]
            latest_slope = eps_latest[1] - eps_latest[0]
            eps_relation = round(eps_average * latest_slope * 100, 2)
            if eps_relation > 50.0:
                eps_score = 5.0
            elif 25.0 < eps_relation <= 50.0:
                eps_score = 4.0
            elif 0.0 < eps_relation <= 25.0:
                eps_score = 3.0
            elif -25.0 < eps_relation <= 0.0:
                eps_score = 2.0
            else:
                eps_score = 1.0
            return eps_score

    def simple_average(self, prices):
       return sum(prices) / len(prices)


class SimpleMA(Model):

    def __init__(self):
        logging.basicConfig(filename='simple_ma.log',
                            level=logging.INFO,
                            format='%(asctime)s %(message)s',
                            datefmt='%H:%M:%S')
        self.daily_trade_symbols = []

    def model_interface(self):
        for symbol in prospects:
            history = broker.get_hist_price(symbol, span='year',
                                            bounds='regular')
            closing_prices = []
            dates = []
            closing_prices = [float(i['close_price']) for i in history]
            last_50 = closing_prices[-50:]
            last_200 = closing_prices[-200:]
            simple_50ma = round(self.simple_average(last_50), 2)
            simple_200ma = round(self.simple_average(last_200), 2)

            # Golden Cross
            if simple_50ma > simple_200ma:
                if not broker.get_open_orders():
                    if symbol not in self.daily_trade_symbols:
                        # IF SYMBOL IN NOT IN daily_trade_symbols
                        quantity = self.order_quantity(symbol)
                        #order_info = broker.market_buy(symbol, quantity, time='gtc')
                        print('Purchasing: %s shares '
                              'of %s' % (str(quantity), symbol))
                        logging.info('Purchasing: %s shares'
                                     ' of %s' % (str(quantity), symbol))
                        self.daily_trade_symbols.append(symbol)
                else:
                    print('Could not purchase: %s due to open order' % symbol)
                    logging.warning('Could not purchase: %s '
                                   'due to open order' % symbol)

            # Death Cross
            elif simple_200ma < simple_50ma:
                # IF SYMBOL IS IN PORTFOLIO SELL ALL SHARES (BUT THIS MIGHT LEAD
                # TO MULTIPLE PURCHASES OF THIS STOCK IN ONE DAY)
                if symbol in self.daily_trade_symbols:
                    print('Selling: %s' % symbol)
                    logging.info('Selling: %s' % symbol)
            else:
              pass

    def simple_average(self, prices):
       return sum(prices) / len(prices)

    def order_quantity(self, symbol):
        '''No single stock shall be greater than 20 Percent of a portfolio
        '''
        buying_power = broker.get_buying_power()
        spread = buying_power * .2
        current_price = broker.get_latest_pricing(symbol)
        current_price = [float(i) for i in current_price]
        shares = int(spread / current_price[0])
        return shares


def main():
    # If portfolio hits the 52 dividend stocks quota start balancing model
    dividend_analyzer = DividendAnalyzer()
    trader_dividend = Trader(dividend_analyzer)

    schedule.every(2).minutes.do(trader_dividend.execute_model)
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
