#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    Simple trading strategy for 'PyAlgoTrade' tutorial
Usage:
    tutorial3
'''

# libraries
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.technical import ma
from pyalgotrade.technical import rsi


# classes
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.__sma = ma.SMA(self.__rsi, 15)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info('%s %s %s' % (bar.getClose(), self.__rsi[-1],
                  self.__sma[-1]))


# executable
if __name__ == '__main__':

    # exec import only
    from docopt import docopt

    # check args
    args = docopt(__doc__)

    # Load the yahoo feed from the csv file
    feed = yahoofeed.Feed()
    feed.addBarsFromCSV('orcl', 'orcl-2000.csv')

    # Evaluate the strategy with the feed's bars
    mystrategy = MyStrategy(feed, 'orcl')
    mystrategy.run()
