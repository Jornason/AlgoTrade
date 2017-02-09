#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    Simple trading strategy from 'PyAlgoTrade' tutorial (see Attribution)
Attribution:
    Gabriel Becedillas 2011-2015
    http://gbeced.github.io/pyalgotrade/docs/v0.18/html/tutorial.html
Usage:
    tutorial2
'''

# libraries
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma


# classes
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        # we want a 15 period SMA over the closing prices
        self.__sma = ma.SMA(feed[instrument].getCloseDataSeries(), 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info('%s %s' % (bar.getClose(), self.__sma[-1]))


# executable
if __name__ == '__main__':

    # exec import only
    from docopt import docopt

    # check args
    args = docopt(__doc__)

    # Load the yahoo feed from the csv file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV('orcl', 'data/orcl-2000.csv')

    # Evaluate the strategy with the feed's bars
    mystrategy = MyStrategy(feed, 'orcl')
    mystrategy.run()
