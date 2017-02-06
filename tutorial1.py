#!/usr/bin/env python

'''
Author: John D. Anderson
Email: jander43@vols.utk.edu
Description:
    Simple trading strategy for 'PyAlgoTrade' tutorial
Usage:
    simple_strategy
'''

# libraries
from pyalgotrade import strategy
from pyalgotrade.barfeed import yahoofeed


# classes
class MyStrategy(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(MyStrategy, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())


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
